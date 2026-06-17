#!/usr/bin/env python3

from pipeline.download_tools import download_tools
from pipeline.write_ninja import write_ninja, Lib
from pathlib import Path
from pipeline.format_symbols import format_symbols
from pipeline.parse_splits import parse_splits
from pipeline.split import split

def Source(matching: bool, name: str) -> tuple[bool, Path]:
    return (matching, Path(name))

NonMatching = False
Matching = True

default_cflags = [
    "-O3",
    "-Ospace",
    "--cpu=MPCore",
    "--split-sections",
]

libs = [
    Lib("tl", default_cflags, [
        #Source(NonMatching, "src/crt0.cpp"), # Doesn't compile correctly
        Source(NonMatching, "src/main.cpp"),
    ]),
]

download_tools()
exheader = Path("orig/exheader")
code = Path("orig/code.bin")

symbols = format_symbols(Path("config/symbols.txt"))
splits = parse_splits(Path("config/splits.txt"))

for s in splits.values():
    split(code, exheader, s, symbols)
write_ninja(libs)
