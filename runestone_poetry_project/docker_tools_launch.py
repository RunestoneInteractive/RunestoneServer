# *********
# |docname|
# *********
# Scripts for Poetry must go here. Use this to redirect to where the script belongs.
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
from docker_tools import cli
