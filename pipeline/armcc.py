# Written by Chloe
# Light wrapper for running armcc, to make ninja script smaller.

import sys
from pathlib import Path
import os
import subprocess

armcc = Path(sys.argv[1])
file = Path(sys.argv[2])
obj = Path(sys.argv[4])

obj.unlink(True)

args = ["tools/wibo"]

if os.name == "nt":
    args.pop()

args += [*sys.argv[1:]]

subprocess.call(args)
