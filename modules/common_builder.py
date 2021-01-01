# ************************************************************
# |docname| - Routines shared between the server and WAF build
# ************************************************************
#
# Imports
# =======
# These are listed in the order prescribed by `PEP 8
# <http://www.python.org/dev/peps/pep-0008/#imports>`_.
#
# Standard library
# ----------------
import atexit
import os
from pathlib import Path
import random
import subprocess
from tempfile import TemporaryDirectory
import threading
import time

# Third-party imports
# -------------------
# None.

# Local imports
# -------------
# None.
#
#
# Globals
# =======
# Set up thread-local storage
_tls = threading.local()


# Simulation scripts and checks
# =============================
# Return the string needed to run a SIM30 simulation.
def get_sim_str_sim30(
    # A string giving the MCU to simulate.
    sim_mcu,
    # The ELF file to load and simulate.
    elf_file,
    # The name of an output file for UART output.
    uart_out_file,
    # Additional, optional commands.
    optional_commands="",
):

    # Spaces in file names break the simulator.
    if " " in elf_file:
        raise ValueError(
            "sim30 does not support spaces in file names, which occurs in {}.".format(
                elf_file
            )
        )

    return (
        # In SIM30, type ? to get help. See also :alink:`the manual <asmguide#page=218>`.
        #
        # .. _supported devices:
        #
        # Select the dsPIC33E. From the help:
        # ``LD <devicename> -Load Device: dspic30super dspic33epsuper pic24epsuper pic24fpsuper pic24super``
        "LD {}\n"
        # Load in the pic24_intro.elf. From the help:
        # ``LC <filename> -Load COFF/ELF File``
        "LC {}\n"
        # Have the simulator save UART1 IO to a file. From the help:
        # ``IO [stdin [stdout]] -Input/Output On (use nul if no stdin and/or stdout)``
        "IO nul {}\n"
        # Reset the processor. From the help:
        # ``RP -Reset processor POR``
        "RP\n"
        # Set a breakpoint at the end of the program (the label ``_done``).
        # From the help:
        # ``BS <location> ...[locations] -Breakpoint Set``
        "BS _done\n"
        # Include any other setup (stimulus file, pin assignments, etc.).
        "{}"
        # Run the program. From the help:
        # ; ``E  -Execute``
        "E 10000\n"
        # Quit. From the help:
        # ``Q  -Quit``
        "Q\n"
    ).format(sim_mcu, elf_file, uart_out_file, optional_commands)


# Return the string needed to run a simulation under MDB.
def get_sim_str_mdb(
    # A string giving the MCU to simulate.
    sim_mcu,
    # The ELF file to load and simulate.
    elf_file,
    # The name of an output file for UART output.
    uart_out_file,
    # Additional, optional commands.
    optional_commands="",
):

    return get_sim_setup_str_mdb(sim_mcu) + get_sim_run_str_mdb(
        elf_file, uart_out_file, optional_commands
    )


# Return the string needed to run a simulation under MDB.
def get_sim_setup_str_mdb(
    # A string giving the MCU to simulate.
    sim_mcu,
):

    return (
        # See :alink:`the MDB manual <http://ww1.microchip.com/downloads/en/DeviceDoc/50002102D.pdf>` for more information.
        #
        # Select the device to simulate.
        "device {}\n"
        # Set up to capture UART 1 output to a file. The simulator produces an error if a file name isn't given here.
        "set uart1io.uartioenabled true\n"
        "set uart1io.output file\n"
        # Configure the clock to match the setup in the PIC24 library ``lib/include/pic24_clockfreq.h`` named ``SIM_CLOCK``.
        "set oscillator.frequency 1\n"
        "set oscillator.frequencyunit Mega\n"
    ).format(sim_mcu)


def get_sim_run_str_mdb(
    # The ELF file to load and simulate.
    elf_file,
    # The name of an output file for UART output.
    uart_out_file,
    # Additional, optional commands.
    optional_commands="",
):

    return (
        # Specify the path to the output file.
        "set uart1io.outputfile {}\n"
        # This is required to get the above setting applied.
        "hwtool sim\n"
        # Load in the program.
        'program "{}"\n'
        # Set a breakpoint at the end of the program (the label ``_done``).
        "break _done\n"
        # Include any other setup (stimulus file, pin assignments, etc.).
        "{}"
        # Run the program. Wait a time in ms for it to finish.
        "run\n"
        "wait 6000\n"
        # In case the wait time expired before encountering a breakpoint, halt the simulation.
        "halt\n"
        # Remove all breakpoints.
        "delete\n"
        # Tell the runner that the simulation is finished.
        "echo Simulation finished.\n"
        # Exit the simulator. For some reason, it takes a while for MDB to exit. This is commented out, so that mdb will stay running until it's shut down after running many sims.
        ##"quit\n"
    ).format(
        # MDB starting in MPLAB X v5.35 doesn't understand Windows-style paths (although using \\ instead of \ does work). It does work with Posix paths.
        Path(uart_out_file).as_posix(),
        Path(elf_file).as_posix(),
        optional_commands,
    )


# Get a verification code (a random, 32-bit value).
def get_verification_code():
    return random.randrange(0, 2 ** 32)


# Returns True if a simulation produced the correct answer.
def check_sim_out(out_str, verification_code):
    sl = out_str.splitlines()
    second_to_last_line = sl[-2] if len(sl) >= 2 else ""
    last_line = sl[-1] if len(sl) >= 1 else ""
    return (second_to_last_line == "Correct.") and (
        last_line == "{}".format(verification_code)
    )


# Run MDB
# =======
# This function runs a simulation, verifying that the simulation results
# are correct, using the newer MDB simulator.
#
# Inputs: path_to_elf_binary
#
# Outputs: sim_output_file
def sim_run_mdb(
    # A path to the MDB script.
    mdb_path,
    # The microcontroller to simulate; for example, "dsPIC33EP128GP502".
    mcu_name,
    # A path to the binary (typically in .elf format) to simulate.
    sim_binary_path,
):

    # Get or create an instance of the simulator.
    po = _tls.__dict__.get("po")
    if (
        # If the simulator hasn't been started, ...
        (not po)
        or
        # ... or it died, (re)create it.
        (po and po.poll() is not None)
    ):

        # Create a temp file for the simulation results. Since the simulator doesn't close the file after the simulation finishes, it can't be deleted. Instead, we need a single file to be used for a simulation, read, then truncated.
        _tls.tempdir = tempdir = TemporaryDirectory()
        _tls.simout_path = Path(_tls.tempdir.name) / "mdb_simout.txt"
        _tls.simout_file = simout_file = open(
            _tls.simout_path, "w+", encoding="utf-8", errors="backslashreplace"
        )

        # Start the simulator.
        po = subprocess.Popen(
            [
                mdb_path,
                # These options must go before the ``--jar`` option, meaning they require hand edits to ``mdb.bat/sh``; they can't be passed as paramters (which are placed after ```--jar`` by ``mdb.bat/sh``.)
                #
                # Per a conversation with Microchip's support team, this disables the start-up check for new language packs, which takes several seconds to complete.
                ##"-Dpackslib.workonline=false",
                # Java, by default, doesn't free memory until it gets low, making this a memory hog. On Windows, it starts up at around 400 MB. This seems to keep it below 600 MB.
                ##"-Xmx750M",
            ],
            text=True,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=os.environ,
        )
        s = get_sim_setup_str_mdb(mcu_name)
        po.stdin.write(s)
        po.stdin.flush()
        _tls.po = po

        def on_exit():
            # Shut down the simulator and end the simulation process.
            po.communicate("quit\n")
            # Remove the simout file.
            simout_file.close()
            tempdir.cleanup()

        atexit.register(on_exit)

    # Delete any previous simulation results.
    _tls.simout_file.truncate(0)

    # Run the simulation.
    s = get_sim_run_str_mdb(sim_binary_path, _tls.simout_path)
    po.stdin.write(s)
    po.stdin.flush()

    # Wait for it to finish by watching stdout.
    time_left = 10
    while time_left > 0:
        line = po.stdout.readline()
        if not line:
            time.sleep(0.1)
            time_left -= 0.1
            continue
        if line == ">/*Simulation finished.*/\n":
            break

    # Read then return the result, starting from the beginning of the file.
    _tls.simout_file.seek(0)
    return _tls.simout_file.read()


# Celery config
# =============
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
