from pathlib import Path
from pipeline.elf import ElfSymbol
from pipeline.elfconsts import STB

def format_symbols(symbol_file: Path) -> dict[int, tuple[ElfSymbol, str]]:
    syms: list[tuple[int, ElfSymbol]] = []
    sym_dict: dict[int, tuple[ElfSymbol, str]] = {}

    orig = symbol_file.read_text()
    for line in orig.splitlines():
        if line.strip():
            sym_addr, attrs = line.split("//")
            sym, addr = sym_addr.split('=')
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

            syms.append((int(addr, 16), symbol))
            sym_dict[int(addr, 16)] = (symbol, mapping)

    syms.sort(key=lambda val: val[0])
    lines = []
    for (addr, sym) in syms:
        match sym.st_info_bind:
            case STB.STB_GLOBAL:
                scope = "global"
            case STB.STB_LOCAL:
                scope = "local"
            case STB.STB_WEAK:
                scope = "weak"
        lines.append(f'{sym.name}={hex(addr)} // size:{hex(sym.st_size)} scope:{scope}')
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
