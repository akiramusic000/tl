#!/usr/bin/env python3

from pipeline.download_tools import download_tools
from pipeline.split_code import split_code
from pipeline.write_ninja import write_ninja, Lib
from pathlib import Path

def Source(matching: bool, name: str) -> tuple[bool, Path]:
    return (matching, Path(name))

NonMatching = False
Matching = True

default_cflags = [
    "-O3",
    "-Ospace",
    "--cpu=MPCore"
]

libs = [
    Lib("tl", default_cflags, [
        #Source(NonMatching, "src/crt0.cpp"), # Doesn't compile correctly
        Source(NonMatching, "src/main.cpp"),
    ]),
]

download_tools()
split_code()
write_ninja(libs)
