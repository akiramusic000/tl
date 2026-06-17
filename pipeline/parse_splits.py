# Module for parsing splits.txt files.
# Written by Chloe.

from pathlib import Path

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Split:
    file_name: str
    symbols: list[int]


def parse_splits(splits_path: Path) -> dict[str, Split]:
    splits = {}

    lines = splits_path.read_text().splitlines()

    for i, line in enumerate(lines):
        if not line:
            continue

        file, addrs = line.split(":")
        symbols = addrs.strip().strip("[]").split(",")
        symbols_clean = []
        for i in symbols:
            if i:
                symbols_clean.append(int(i.strip(), 16))
        
        splits[file] = Split(file, symbols_clean)

    return splits
