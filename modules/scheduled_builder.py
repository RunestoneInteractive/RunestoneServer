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
import shutil
from io import open
import sys

# Third-party imports
# -------------------
from celery import Celery
from runestone.lp.lp_common_lib import BUILD_SYSTEM_PATH, get_sim_str_sim30

try:
    # This can't be imported from uwsgi, but isn't needed there either.
    from gevent import subprocess
except:
    pass

# Local imports
# -------------
# None.


# Create the Celery app.
app = Celery(
    "scheduled_builder",
    backend="rpc://",
    broker=os.environ.get("REDIS_URI", "redis://localhost:6379/0"),
)

app.conf.update(result_expires=120)

# This function should run the provided code and report the results. It will
# vary for a given compiler and language.
@app.task(name="scheduled_builder._scheduled_builder")
def _scheduled_builder(
    # The name of the builder to use.
    builder,
    # An absolute path to the file which contains code to test. The file resides in a
    # temporary directory, which should be used to hold any additional files
    # produced by the test.
    file_path,
    # An absolute path to the Sphinx root directory.
    sphinx_base_path,
    # A relative path to the Sphinx source path from the ``sphinx_base_path``.
    sphinx_source_path,
    # A relative path to the Sphinx output path from the ``sphinx_base_path``.
    sphinx_out_path,
    # A relative path to the source file from the ``sphinx_source_path``, based
    # on the submitting web page.
    source_path,
):

    if builder == "unsafe-python" and os.environ.get("WEB2PY_CONFIG") == "test":
        # Run the test in Python. This is for testing only, and should never be used in production; instead, this should be run in a limited Docker container. For simplicity, it lacks a timeout.
        #
        # First, copy the test to the temp directory. Otherwise, running the test file from its book location means it will import the solution, which is in the same directory.
        cwd = os.path.dirname(file_path)
        test_file_name = os.path.splitext(os.path.basename(file_path))[0] + "-test.py"
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
        try:
            str_out = subprocess.check_output(
                [sys.executable, dest_test_path],
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=cwd,
            )
            return str_out, 100
        except subprocess.CalledProcessError as e:
            # from gluon.debug import dbg; dbg.set_trace()
            return e.output, 0
    elif builder != "pic24-xc16-bullylib":
        raise RuntimeError("Unknown builder {}".format(builder))

    # Assemble or compile the source. We assume that the binaries are already in the path.
    xc16_path = ""
    # Compile in the temporary directory, in which ``file_path`` resides.
    sp_args = dict(
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        cwd=os.path.dirname(file_path),
    )
    o_path = file_path + ".o"
    extension = os.path.splitext(file_path)[1]
    if extension == ".s":
        args = [
            os.path.join(xc16_path, "xc16-as"),
            "-omf=elf",
            "-g",
            "--processor=33EP128GP502",
            file_path,
            "-o" + o_path,
        ]
    elif extension == ".c":
        args = [
            os.path.join(xc16_path, "xc16-gcc"),
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
            file_path,
            "-c",
            "-o" + o_path,
        ]
    else:
        raise RuntimeError("Unknown file extension in {}.".format(file_path))
    out = _subprocess_string(args, **sp_args)
    try:
        out += subprocess.check_output(args, **sp_args)
    except subprocess.CalledProcessError as e:
        out += e.output
        return out, 0

    # Link.
    elf_path = file_path + ".elf"
    waf_root = os.path.normpath(
        os.path.join(
            sphinx_base_path, sphinx_out_path, BUILD_SYSTEM_PATH, sphinx_source_path
        )
    )
    test_object_path = os.path.join(
        waf_root, os.path.splitext(source_path)[0] + "-test.c.1.o"
    )
    args = [
        os.path.join(xc16_path, "xc16-gcc"),
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
        "-o" + elf_path,
        "-Wl,-Bstatic",
        "-Wl,-Bdynamic",
    ]
    out += "\n" + _subprocess_string(args, **sp_args)
    try:
        out += subprocess.check_output(args, **sp_args)
    except subprocess.CalledProcessError as e:
        out += e.output
        return out, 0

    # Simulate. Create the simulation commands.
    simout_path = file_path + ".simout"
    ss = get_sim_str_sim30("dspic33epsuper", elf_path, simout_path)
    # Run the simulation. This is a re-coded version of ``wscript.sim_run`` -- I
    # couldn't find a way to re-use that code.
    sim_ret = 0
    args = [os.path.join(xc16_path, "sim30")]
    out += "\nTest results:\n" + _subprocess_string(args, **sp_args)
    try:
        cp = subprocess.run(
            args, input=ss, stdout=subprocess.PIPE, timeout=5, **sp_args
        )
        sim_ret = cp.returncode
    except subprocess.TimeoutExpired:
        sim_ret = 1
        timeout_str = "\n\nTimeout."
    else:
        timeout_str = ""
    with open(simout_path, encoding="utf-8") as f:
        out += f.read().rstrip()
    # Put the timeout string at the end of all the simulator output.
    out += timeout_str
    return out, (100 if not sim_ret and out.endswith("Correct.") else 0)


# Transform the arguments to ``subprocess.run`` into a string showing what
# command will be executed.
def _subprocess_string(*args, **kwargs):
    return kwargs.get("cwd", "") + "% " + " ".join(args[0]) + "\n"
