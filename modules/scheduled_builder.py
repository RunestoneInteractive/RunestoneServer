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
from io import open
import os
import shutil
import subprocess
import sys
import threading

# Third-party imports
# -------------------
from celery import Celery
from celery.utils.log import current_process_index
from runestone.lp.lp_common_lib import BUILD_SYSTEM_PATH
from common_builder import (
    get_sim_str_sim30,
    sim_run_mdb,
    get_verification_code,
    check_sim_out,
)

# Local imports
# -------------
# None.


# Celery
# ======
# Provide the `Celery configuration <https://docs.celeryproject.org/en/latest/userguide/application.html#configuration>`_.
celery_config = dict(
    # Use `Redis with Celery <http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html#configuration>`_.
    broker_url=os.environ.get("REDIS_URI", "redis://localhost:6379/0"),
    result_backend=os.environ.get("REDIS_URI", "redis://localhost:6379/0"),
    # Given that tasks time out in 60 seconds, expire them after that. See `result_expires <https://docs.celeryproject.org/en/latest/userguide/configuration.html#result-expires>`.
    result_expires=120,
    # This follows the `Redis caveats <http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html#redis-caveats>`_.
    broker_transport_options={
        # 1 hour.
        "visibility_timeout": 3600,
        "fanout_prefix": True,
        "fanout_patterns": True,
    },
)


# Create and configure the Celery app.
app = Celery("scheduled_builder")
app.conf.update(celery_config)


# Provide a Celery task to run mdb. This is used when externally compiling code in a book; it's not used by the webserver.
@app.task
def celery_sim_run_mdb(*args, **kwargs):
    return sim_run_mdb(*args, **kwargs)


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
        "python": python_builder,
        "rust": rust_builder,
        "pic24-xc16-bullylib": xc16_builder,
        "armv7-newlib-sim": armv7_builder,
    }.get(builder, None)
    if builder_func is None:
        raise RuntimeError(f"Unknown builder {builder}")

    # Run the builder then return the results.
    try:
        out_list, correct = builder_func(
            file_path,
            os.path.dirname(file_path),
            sphinx_base_path,
            sphinx_source_path,
            sphinx_out_path,
            source_path,
        )
    except BuildFailed as e:
        out_list = e.out_list
        correct = e.correct
    return "".join(out_list), correct


# Utilities
# =========
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
    # True if stderr should be included in the results.
    include_stderr=True,
    # Additional kwargs for the subprocess call.
    **kwargs,
):
    out_list.extend(
        [
            # Add a newline before the next title, unless there's nothing in the output list yet.
            "\n" if out_list else "",
            # Print the title with a nice underline.
            f"{desc}\n{'=' * len(desc)}\n",
            # Show the command executed.
            _subprocess_string(args, cwd=cwd),
        ]
    )

    try:
        cp = subprocess.run(
            args, capture_output=True, text=True, cwd=cwd, timeout=15, *kwargs
        )
    except subprocess.TimeoutExpired as e:
        cp = e
        # Create a failing return code for the logic below.
        cp.returncode = True

    # Record output if available.
    if cp.stdout:
        out_list.append(cp.stdout)
    if include_stderr and cp.stderr:
        out_list.append(cp.stderr)
    # Put the timeout message last.
    if cp.returncode is True:
        out_list.append("Timeout.\n\n")

    # A returncode of 0 indicates success; anything else is an error.
    if cp.returncode:
        raise BuildFailed(out_list, 0)
    return out_list, 100


# Copy the test file from its Sphinx location to the temporary directory where the student source code is. Return the name of the test file; if the copy failed, assume there's no test file; instead, return the file name of the student source code.
def copy_test_file_to_tmp(
    file_path, cwd, sphinx_base_path, sphinx_source_path, source_path, ext=None
):
    # If not provided, assume the test file's extension is the same as the student source file.
    if not ext:
        ext = os.path.splitext(file_path)[1]
    # The test file name takes file_name.old_ext and produces file_name-test.new_ext.
    test_file_name = os.path.splitext(os.path.basename(file_path))[0] + f"-test{ext}"
    dest_test_path = os.path.join(cwd, test_file_name)
    try:
        shutil.copyfile(
            os.path.join(
                sphinx_base_path,
                sphinx_source_path,
                os.path.dirname(source_path),
                test_file_name,
            ),
            dest_test_path,
        )
    except OSError:
        # The test file couldn't be copied; assume the test should run on the student source file instead.
        return os.path.basename(file_path)
    return test_file_name


# Given an list of arguments to pass as the first parameter of ``subprocess.run``, wrap this in runguard. Return an updates list of parameters for ``subprocess.run``.
def runguard(
    # A list of arguments comprising the first parameter of ``subprocess.run``.
    args,
    # The directory containing the executable to run in runguard.
    cwd,
    # Kill COMMAND after TIME seconds (float).
    time_s=15,
    # Set maximum CPU time to TIME seconds (float).
    cputime_s=10,
    # Set all (total, stack, etc) memory limits to SIZE kB.
    memsize_kb=100,
    # Set maximum created filesize to SIZE kB.
    filesize_kb=50,
    # Set maximum no. processes to N.
    num_processes=1,
    # Disable core dumps when True
    no_core_dumps=True,
):
    # Get (hopefully) the `prefork pool process index <https://docs.celeryproject.org/en/stable/userguide/workers.html#prefork-pool-process-index>`_. Use this to select a jobe userid that's not in use. Since it only applies to prefork pools, use a thread ID as backup.
    user = f"jobe{current_process_index() or (threading.get_ident() % 10):02d}"
    # Give the selected Jobe user access. Inspired by `jobe source <https://github.com/trampgeek/jobe/blob/master/application/libraries/LanguageTask.php>`_.
    subprocess.run(["setfacl", "-m", f"u:{user}:rwX", cwd], check=True)
    return (
        [
            "sudo",
            "/var/www/jobe/runguard/runguard",
            f"--user={user}",
            "--group=jobe",
            f"--time={time_s}",
            f"--cputime={cputime_s}",
            f"--memsize={memsize_kb}",
            f"--filesize={filesize_kb}",
            f"--nproc={num_processes}",
        ]
        + (["--no_core"] if no_core_dumps else [])
        + args
    )


# Builders
# ========
def python_builder(
    file_path, cwd, sphinx_base_path, sphinx_source_path, sphinx_out_path, source_path
):
    # Copy the test to the temp directory. Otherwise, running the test file from its book location means it will import the solution, which is in the same directory.
    run_file_name = copy_test_file_to_tmp(
        file_path, cwd, sphinx_base_path, sphinx_source_path, source_path
    )

    return report_subprocess(
        runguard([sys.executable, run_file_name], cwd), "Run", cwd, []
    )


def rust_builder(
    file_path, cwd, sphinx_base_path, sphinx_source_path, sphinx_out_path, source_path
):
    # First, copy the test to the temp directory. Otherwise, running the test file from its book location means it will import the solution, which is in the same directory.
    run_file_name = copy_test_file_to_tmp(
        file_path, cwd, sphinx_base_path, sphinx_source_path, source_path
    )

    # Compile. See `rustc tests <https://doc.rust-lang.org/rustc/tests/index.html>`_.
    out_list = []
    report_subprocess(["rustc", "--test", run_file_name], "Compile", cwd, out_list)

    # Run.
    return report_subprocess(
        runguard(["./" + os.path.splitext(run_file_name)[0]], cwd), "Run", cwd, out_list
    )


def xc16_builder(
    file_path, cwd, sphinx_base_path, sphinx_source_path, sphinx_out_path, source_path
):
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
    test_object_path = file_path + ".test.o"
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
        "-lpic24_stdlib",
        "-L" + os.path.join(waf_root, ".."),
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
    file_path, cwd, sphinx_base_path, sphinx_source_path, sphinx_out_path, source_path
):
    # Assemble or compile the source. We assume that the binaries are already in the path.
    o_path = file_path + ".o"
    # Compile and link the source file. The most helpful resource I've found on bare-metal ARM with newlib: https://jasonblog.github.io/note/arm_emulation/simplest_bare_metal_program_for_arm.html. However, I prefer this (simpler) approach.
    args = [
        "arm-none-eabi-gcc",
        # The student source.
        file_path,
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

    lib_path = os.path.join(
        sphinx_base_path,
        sphinx_source_path,
    )
    test_file_path = os.path.join(
        lib_path,
        os.path.splitext(source_path)[0] + "-test.c",
    )
    test_object_path = file_path + ".test.o"

    # Build the test code with a random verification code.
    args = [
        "arm-none-eabi-gcc",
        # The test code.
        test_file_path,
        # Pass the verification code. TODO: separate compiles, so user code doesn't have this value.
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
        "-c",
        "-o" + test_object_path,
    ]
    report_subprocess(args, "Compile test code", cwd, out_list)

    # Link.
    elf_path = file_path + ".elf"
    args = [
        "arm-none-eabi-gcc",
        # Compiled sources.
        o_path,
        test_object_path,
        # Output args.
        "-o",
        elf_path,
        # The ARM needs an interrupt vector table defined for this specific processor. It doesn't work if placed in the library below.
        os.path.join(
            sphinx_base_path,
            sphinx_source_path,
            "tests/platform/ARMv7-A_ARMv7-R/interrupts.S",
        ),
        # Include the ARM library.
        "-larmv7_stdlib",
        "-L" + os.path.join(waf_root, ".."),
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
    report_subprocess(args, "Link", cwd, out_list)

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
    out_list, correct = report_subprocess(
        args, "Simulate", cwd, out_list, include_stderr=False
    )

    return out_list, (
        100 if correct == 100 and check_sim_out(out_list, verification_code) else 0
    )
