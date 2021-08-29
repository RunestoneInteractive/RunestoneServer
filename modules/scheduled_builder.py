# ************************************************
# |docname| - Provide feedback for student answers
# ************************************************
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
import os
import subprocess
import shutil
from io import open
import sys

# Third-party imports
# -------------------
from celery import Celery
from runestone.lp.lp_common_lib import BUILD_SYSTEM_PATH
from common_builder import (
    get_sim_str_sim30,
    sim_run_mdb,
    get_verification_code,
    check_sim_out,
    celery_config,
)

# Local imports
# -------------
# None.


# Utilities
# =========
# Create and configure the Celery app.
app = Celery("scheduled_builder")
app.conf.update(celery_config)


# This function should run the provided code and report the results. It will
# vary for a given compiler and language.
@app.task(name="scheduled_builder._scheduled_builder")
def _scheduled_builder(
    # The name of the builder to use.
    builder,
    # An absolute path to the file which contains code to test. The file resides in a temporary directory, which should be used to hold any additional files produced by the test.
    file_path,
    # An absolute path to the Sphinx root directory.
    sphinx_base_path,
    # A relative path to the Sphinx source path from the ``sphinx_base_path``.
    sphinx_source_path,
    # A relative path to the Sphinx output path from the ``sphinx_base_path``.
    sphinx_out_path,
    # A relative path to the source file from the ``sphinx_source_path``, based on the submitting web page.
    source_path,
):

    # Translate the provided builder into a Python function.
    builder_func = {
        "unsafe-python": python_builder,
        "unsafe-rust": rust_builder,
        "pic24-xc16-bullylib": xc16_builder,
        "armv7-newlib-sim": armv7_builder,
    }.get(builder, None)
    # The Python builder is for testing only. TODO: Run this in JOBE instead.
    if builder == "unsafe-python" and os.environ.get("WEB2PY_CONFIG") != "test":
        builder_func = None

    if builder_func is None:
        raise RuntimeError("Unknown builder {}".format(builder))

    try:
        out_list, correct = builder_func(
            file_path,
            sphinx_base_path,
            sphinx_source_path,
            sphinx_out_path,
            source_path,
        )
    except BuildFailed as e:
        out_list = e.out_list
        correct = e.correct
    return "".join(out_list), correct


# Raise this exception if the build fails.
class BuildFailed(Exception):
    def __init__(self, out_list, correct=0):
        self.out_list = out_list
        self.correct = correct


# Transform the arguments to ``subprocess.run`` into a string showing what
# command will be executed.
def _subprocess_string(args, **kwargs):
    return kwargs.get("cwd", "") + "% " + " ".join(args) + "\n"


# Run a subprocess with the provided arguments, returning a string which contains the output. On failure, raise an exception. Returns True if the subprocess completed successfully.
def report_subprocess(
    # Arguments to invoke the subprocess.
    args,
    # A string describing this step in the build.
    desc,
    # A path to the working directory for the subprocess.
    cwd,
    # A list of output produced thus far in the build; this function will append to it.
    out_list,
    # True if stdout should be included in the results.
    include_stdout=True,
    # Additional kwargs for the subprocess call.
    **kwargs,
):
    # Add a newline before the next title, unless there's nothing in the output list yet.
    if out_list:
        out_list.append("\n")
    out_list.extend([f"{desc}\n{'=' * len(desc)}\n", _subprocess_string(args, cwd=cwd)])

    try:
        cp = subprocess.run(
            args, capture_output=True, text=True, cwd=cwd, timeout=15, *kwargs
        )
    except subprocess.TimeoutExpired as e:
        cp = e
        # Create a failing return code for the logic below.
        cp.returncode = -1
        out_list.append("Timeout.\n\n")

    # Record output.
    out_list.append(cp.stdout)
    if include_stdout:
        out_list.append(cp.stderr)

    # A returncode of 0 indicates success; anything else is an error.
    if cp.returncode:
        raise BuildFailed(out_list, 0)
    return out_list, 100


# Given a path to the student source, determine the name of the corresponding test file.
def get_test_file_name(file_path, ext):
    return os.path.splitext(os.path.basename(file_path))[0] + f"-test{ext}"


# Copy the test file from its Sphinx location to the temporary directory where the student source code is.
def copy_test_file_to_tmp(
    test_file_name, cwd, sphinx_base_path, sphinx_source_path, source_path
):
    dest_test_path = os.path.join(cwd, test_file_name)
    shutil.copyfile(
        os.path.join(
            sphinx_base_path,
            sphinx_source_path,
            os.path.dirname(source_path),
            test_file_name,
        ),
        dest_test_path,
    )


# Builders
# ========
def python_builder(
    file_path, sphinx_base_path, sphinx_source_path, sphinx_out_path, source_path
):
    cwd = os.path.dirname(file_path)

    # Copy the test to the temp directory. Otherwise, running the test file from its book location means it will import the solution, which is in the same directory.
    test_file_name = get_test_file_name(file_path, ".py")
    copy_test_file_to_tmp(
        test_file_name, cwd, sphinx_base_path, sphinx_source_path, source_path
    )

    return report_subprocess([sys.executable, dest_test_path], "Run Python", cwd, [])


def rust_builder(
    file_path, sphinx_base_path, sphinx_source_path, sphinx_out_path, source_path
):
    cwd = os.path.dirname(file_path)

    # First, copy the test to the temp directory. Otherwise, running the test file from its book location means it will import the solution, which is in the same directory.
    test_file_name = get_test_file_name(file_path, ".rs")
    copy_test_file_to_tmp(
        test_file_name, cwd, sphinx_base_path, sphinx_source_path, source_path
    )

    # Compile. See `rustc tests <https://doc.rust-lang.org/rustc/tests/index.html>`_.
    out_list = []
    report_subprocess(["rustc", "--test", test_file_name], "Compile", cwd, out_list)

    # Run.
    return report_subprocess(
        ["./" + os.path.splitext(test_file_name)[0]], "Run", cwd, out_list
    )


def xc16_builder(
    file_path, sphinx_base_path, sphinx_source_path, sphinx_out_path, source_path
):
    cwd = os.path.dirname(file_path)

    # Assemble or compile the source. We assume that the binaries are already in the path.
    o_path = file_path + ".o"
    extension = os.path.splitext(file_path)[1]
    try:
        is_extension_asm = {".s": True, ".c": False}[extension]
    except Exception:
        raise RuntimeError("Unknown file extension in {}.".format(file_path))
    if is_extension_asm:
        args = [
            "xc16-as",
            "-omf=elf",
            "-g",
            "--processor=33EP128GP502",
            file_path,
            "-o" + o_path,
        ]
    else:
        args = [
            "xc16-gcc",
            "-mcpu=33EP128GP502",
            "-omf=elf",
            "-g",
            "-O0",
            "-msmart-io=1",
            "-Wall",
            "-Wextra",
            "-Wdeclaration-after-statement",
            "-I" + os.path.join(sphinx_base_path, sphinx_source_path, "lib/include"),
            "-I" + os.path.join(sphinx_base_path, sphinx_source_path, "tests"),
            "-I"
            + os.path.join(
                sphinx_base_path, sphinx_source_path, "tests/platform/Microchip_PIC24"
            ),
            "-I"
            + os.path.join(
                sphinx_base_path, sphinx_source_path, os.path.dirname(source_path)
            ),
            "-DSIM",
            file_path,
            "-c",
            "-o" + o_path,
        ]
    out_list = []
    report_subprocess(args, "Compile / Assemble", cwd, out_list)

    # Build the test code with a random verification code.
    verification_code = get_verification_code()
    waf_root = os.path.normpath(
        os.path.join(
            sphinx_base_path, sphinx_out_path, BUILD_SYSTEM_PATH, sphinx_source_path
        )
    )
    test_file_path = os.path.join(
        sphinx_base_path,
        sphinx_source_path,
        os.path.splitext(source_path)[0] + "-test.c",
    )
    test_object_path = os.path.join(
        waf_root,
        "{}-test.c.{}.o".format(os.path.splitext(source_path)[0], verification_code),
    )
    args = [
        "xc16-gcc",
        "-mcpu=33EP128GP502",
        "-omf=elf",
        "-g",
        "-O0",
        "-msmart-io=1",
        "-Wall",
        "-Wextra",
        "-Wdeclaration-after-statement",
        "-I" + os.path.join(sphinx_base_path, sphinx_source_path, "lib/include"),
        "-I" + os.path.join(sphinx_base_path, sphinx_source_path, "tests"),
        "-I"
        + os.path.join(
            sphinx_base_path, sphinx_source_path, "tests/platform/Microchip_PIC24"
        ),
        "-I"
        + os.path.join(
            sphinx_base_path, sphinx_source_path, os.path.dirname(source_path)
        ),
        test_file_path,
        "-DSIM",
        "-DVERIFICATION_CODE=({}u)".format(verification_code),
        "-c",
        "-o" + test_object_path,
    ]
    report_subprocess(args, "Compile test code", cwd, out_list)

    # Link.
    elf_path = file_path + ".elf"
    args = [
        "xc16-gcc",
        "-omf=elf",
        "-Wl,--heap=100,--stack=16,--check-sections,--data-init,--pack-data,--handles,--isr,--no-gc-sections,--fill-upper=0,--stackguard=16,--no-force-link,--smart-io",
        "-Wl,--script="
        + os.path.join(
            sphinx_base_path, sphinx_source_path, "lib/lkr/p33EP128GP502_bootldr.gld"
        ),
        test_object_path,
        o_path,
        os.path.join(waf_root, "lib/src/pic24_clockfreq.c.1.o"),
        os.path.join(waf_root, "lib/src/pic24_configbits.c.1.o"),
        os.path.join(waf_root, "lib/src/pic24_serial.c.1.o"),
        os.path.join(waf_root, "lib/src/pic24_timer.c.1.o"),
        os.path.join(waf_root, "lib/src/pic24_uart.c.1.o"),
        os.path.join(waf_root, "lib/src/pic24_util.c.1.o"),
        os.path.join(waf_root, "tests/test_utils.c.1.o"),
        os.path.join(waf_root, "tests/test_assert.c.1.o"),
        os.path.join(waf_root, "tests/coroutines.c.1.o"),
        os.path.join(waf_root, "tests/platform/Microchip_PIC24/platform.c.1.o"),
        "-o" + elf_path,
    ]
    report_subprocess(args, "Link", cwd, out_list)

    # Simulate. Create the simulation commands.
    sim_ret = 0
    if not is_extension_asm:
        out_list.append(sim_run_mdb("mdb", "dspic33EP128GP502", elf_path))
    else:
        simout_path = file_path + ".simout"
        timeout_str = ""
        ss = get_sim_str_sim30("dspic33epsuper", elf_path, simout_path)
        args = ["sim30"]

        # Run the simulation. This is a re-coded version of ``wscript.sim_run`` -- I couldn't find a way to re-use that code.
        sp_args = dict(
            stderr=subprocess.STDOUT,
            text=True,
            cwd=cwd,
        )
        out_list.extend(
            ["\nSimulation\n==========\n", _subprocess_string(args, **sp_args)]
        )
        try:
            cp = subprocess.run(
                args, input=ss, stdout=subprocess.PIPE, timeout=10, **sp_args
            )
            sim_ret = cp.returncode
        except subprocess.TimeoutExpired:
            sim_ret = 1
            timeout_str = "\n\nTimeout."

        # Read the results of the simulation.
        try:
            with open(simout_path, encoding="utf-8", errors="backslashreplace") as f:
                out_list.append(f.read().rstrip())
        except Exception as e:
            out_list(f"No simulation output produced in {simout_path} - {e}.\n")
        # Put the timeout string at the end of all the simulator output.
        if timeout_str:
            out_list.append(timeout_str)

    return out_list, (
        100 if not sim_ret and check_sim_out(out_list, verification_code) else 0
    )


def armv7_builder(
    file_path, sphinx_base_path, sphinx_source_path, sphinx_out_path, source_path
):
    cwd = os.path.dirname(file_path)
    # Build the test code with a random verification code.
    verification_code = get_verification_code()

    # Assemble or compile the source. We assume that the binaries are already in the path.
    elf_path = file_path + ".elf"
    lib_path = os.path.join(
        sphinx_base_path,
        sphinx_source_path,
    )
    test_file_path = os.path.join(
        lib_path,
        os.path.splitext(source_path)[0] + "-test.c",
    )

    # Compile and link the source file. The most helpful resource I've found on bare-metal ARM with newlib: https://jasonblog.github.io/note/arm_emulation/simplest_bare_metal_program_for_arm.html. However, I prefer this (simpler) approach.
    args = [
        "arm-none-eabi-gcc",
        # The student source.
        file_path,
        # The test code.
        test_file_path,
        # Output args.
        "-o",
        elf_path,
        # Pass the verification code.
        "-DVERIFICATION_CODE=({}u)".format(verification_code),
        # Provide picky warnings, etc.
        "-g",
        "-O0",
        "-Wall",
        "-Wextra",
        "-Wdeclaration-after-statement",
        # Include paths for the book.
        "-I" + os.path.join(sphinx_base_path, sphinx_source_path, "lib/include"),
        "-I" + os.path.join(sphinx_base_path, sphinx_source_path, "tests"),
        "-I"
        + os.path.join(
            sphinx_base_path, sphinx_source_path, "tests/platform/ARMv7-A_ARMv7-R"
        ),
        "-I"
        + os.path.join(
            sphinx_base_path, sphinx_source_path, os.path.dirname(source_path)
        ),
        # Book library files. TODO: compile these into a library and link with that instead for efficiency.
        os.path.join(lib_path, "tests/test_utils.c"),
        os.path.join(lib_path, "tests/test_assert.c"),
        os.path.join(lib_path, "tests/platform/ARMv7-A_ARMv7-R/platform.c"),
        # The ARM needs an interrupt vector table defined for this specific processor.
        os.path.join(
            sphinx_base_path,
            sphinx_source_path,
            "tests/platform/ARMv7-A_ARMv7-R/interrupts.S",
        ),
        # The custom linker file defines a section to correctly place these interrupt vectors.
        "-T",
        os.path.join(
            sphinx_base_path,
            sphinx_source_path,
            "tests/platform/ARMv7-A_ARMv7-R/redboot.ld",
        ),
        # Use the RDIMON semihosting tools to provide the standard library (write, exit, etc.).
        "--specs=/usr/lib/arm-none-eabi/newlib/aprofile-ve.specs",
        # The specific chip we use has a different RAM address than the linker file. Override it here.
        "-Wl,--section-start=.text=0x60010000",
    ]
    out_list = []
    report_subprocess(args, "Build", cwd, out_list)

    # Transform to a bin file.
    bin_path = file_path + ".bin"
    report_subprocess(
        ["arm-none-eabi-objcopy", "-O", "binary", elf_path, bin_path],
        "Transform to bin",
        cwd,
        out_list,
    )

    # Simulate.
    args = [
        # QEMU provides `fairly good simulation for ARM <https://qemu-project.gitlab.io/qemu/system/target-arm.html>`_. For more of the following options, search the `QEMU invocation <https://qemu-project.gitlab.io/qemu/system/invocation.html>`_ page.
        "qemu-system-arm",
        # Pick a specific system, in this case the `ARM Versatile Express-A9 <https://qemu-project.gitlab.io/qemu/system/arm/vexpress.html>`_
        "-M",
        "vexpress-a9",
        # Give the processor 32 MB of RAM. Search for ``-m [size=]`` on the `QEMU invocation`_ page.
        "-m",
        "32M",
        # Does this even matter?
        "-no-reboot",
        # Run only from the command line instead of displaying a QEMU GUI plus graphics from the emulated system.
        "-nographic",
        # Even with this option, QEMU complains about command-line options. ???
        "-audiodev",
        "id=none,driver=none",
        # Reserve stdio for I/O from the emulated system, instead of the monitor.
        "-monitor",
        "none",
        # The binary is loaded as if it's a Linux kernel.
        "-kernel",
        bin_path,
        # Send all ARM I/O to the console.
        "-serial",
        "stdio",
        # Enable semihosting, so that newlib can easily exit the simulator, produce stdio, etc.
        "-semihosting",
    ]
    out_list, correct = report_subprocess(args, "Simulate", cwd, out_list, include_stdout=False)

    return out_list, (
        100 if correct == 100 and check_sim_out(out_list, verification_code) else 0
    )
