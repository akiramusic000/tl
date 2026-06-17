# Script to format symbols.txt.
# Written by Chloe (with edits from RootCubed), taken from https://github.com/RootCubed/mwcceppc-decomp.

from pathlib import Path
from pipeline.elf import ElfSymbol
from pipeline.elfconsts import STB
from dataclasses import dataclass

@dataclass
class Symbol:
    elf_symbol: ElfSymbol
    mapping: str
    section: str

def format_symbols(symbol_file: Path) -> dict[int, Symbol]:
    syms: list[tuple[int, Symbol]] = []
    sym_dict: dict[int, Symbol] = {}

    orig = symbol_file.read_text()
    for line in orig.splitlines():
        if line.strip():
            sym_addr, attrs = line.split("//")
            sym, section_addr = sym_addr.split('=')
            section, addr = section_addr.strip().strip(";").split(":")
            if sym in syms:
                print('Warning: symbol', sym, 'defined multiple times in', symbol_file.name, end='!\n')
            symbol = ElfSymbol(sym)
            attrs = attrs.split()

            mapping = "$a"

            for attr in attrs:
                name, value = attr.split(":")
                match name:
                    case "size":
                        symbol.st_size = int(value, 16)
                    case "scope":
                        match value:
                            case "global":
                                symbol.st_info_bind = STB.STB_GLOBAL
                            case "local":
                                symbol.st_info_bind = STB.STB_LOCAL
                            case "weak":
                                symbol.st_info_bind = STB.STB_WEAK
                    case "type":
                        mapping = value

            syms.append((int(addr, 16), Symbol(symbol, mapping, section)))
            sym_dict[int(addr, 16)] = Symbol(symbol, mapping, section)

    syms.sort(key=lambda val: val[0])
    lines = []
    for (addr, symbol) in syms:
        elf_symbol = symbol.elf_symbol
        match elf_symbol.st_info_bind:
            case STB.STB_GLOBAL:
                scope = "global"
            case STB.STB_LOCAL:
                scope = "local"
            case STB.STB_WEAK:
                scope = "weak"
        lines.append(f'{elf_symbol.name}={symbol.section}:{hex(addr)}; // size:{hex(elf_symbol.st_size)} scope:{scope} mapping:{symbol.mapping}')
    formatted = '\n'.join(lines)

    if orig != formatted:
        symbol_file.write_text(formatted)

    return sym_dict

if __name__ == '__main__':
    # Parse arguments separately so this file can be imported from other ones
    import argparse
    parser = argparse.ArgumentParser(description='Formats symbol files.')
    parser.add_argument('symbol_file', type=Path, help='Symbol file to be formatted.')
    args = parser.parse_args()
    format_symbols(args.symbol_file)
