from pathlib import Path
from pipeline.format_symbols import format_symbols
from pipeline.parse_splits import parse_splits
from pipeline.split import split

def split_code():
    exheader = Path("orig/exheader")
    code = Path("orig/code.bin")

    symbols = format_symbols(Path("config/symbols.txt"))
    splits = parse_splits(Path("config/splits.txt"))

    for s in splits.values():
        split(code, exheader, s, symbols)