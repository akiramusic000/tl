from pathlib import Path

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Split:
    file_name: str
    sections: dict[str, tuple[int, int]]


def parse_splits(splits_path: Path) -> dict[str, Split]:
    splits = {}

    lines = splits_path.read_text().splitlines()
    file = None
    sections: dict[str, tuple[int, int]] = {}

    for i, line in enumerate(lines):
        if line.endswith(":"):
            if file != None:
                splits[file] = Split(file, sections)
            file = line.removesuffix(":")
            sections = {}
        elif line == "":
            continue
        else:
            if file == None:
                raise Exception(f"Section not attached to file! ({splits_path}:{i})")

            parts = line.split()
            section = parts[0]
            start = int(parts[1].removeprefix("start:"), base=16)
            end = int(parts[2].removeprefix("end:"), base=16)

            sections[section] = (start, end)

    if file != None:
        splits[file] = Split(file, sections)

    return splits
