# Module for splitting code.bin.
# Written (roughly and messily) by Chloe.

from pathlib import Path
from pipeline.format_symbols import Symbol
from pipeline.parse_splits import Split
from pipeline.elf import ElfSection, ElfFile, ElfSymbol, ElfSymtab, ElfRela, ElfRelaSec
from pipeline.elfconsts import ET, EM, ARM_RELOC_TYPE, SpecialSections
import capstone
import os

def split(code_bin: Path, exheader: Path, split: Split, symbols: dict[int, Symbol]):
    code_bin_file = code_bin.open("rb")
    exheader_file = exheader.open("rb")
    exheader_file.seek(0x10, os.SEEK_SET)
    base_address = int.from_bytes(exheader_file.read(4), byteorder="little")

    elf = ElfFile(ET.ET_REL, EM.EM_ARM)
    elf_symbol_table = ElfSymtab()
    elf.add_section(elf_symbol_table)

    section_idx = 2

    md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_LITTLE_ENDIAN)
    md.detail = True
    md.skipdata = True

    for split_symbol_addr in split.symbols:
        mappings: dict[int, str] = {}

        def add_mapping(offset: int, type: str):
            if offset not in mappings or mappings[offset] != "$a":
                mappings[offset] = type

        symbol = symbols[split_symbol_addr]
        elf_symbol = symbol.elf_symbol
        start = split_symbol_addr
        end = start + elf_symbol.st_size
        section = symbol.section if symbol.section != ".text" else "i." + elf_symbol.name

        symbol.elf_symbol.st_shndx = section_idx

        add_mapping(0, symbol.mapping)
        elf_symbol_table.syms.append(symbol.elf_symbol)

        in_code = True
        current_func = start
        next_func = current_func + elf_symbol.st_size

        if symbol.section == ".text":
            elf_relocs = ElfRelaSec(f'.rela.{section}')
            elf_relocs.header.sh_info = section_idx
            elf_relocs.header.sh_link = 1

        code_bin_file.seek(start - base_address, os.SEEK_SET)
        split_bytes = code_bin_file.read(end - start)
        elf_section = ElfSection(section, split_bytes)
        h_type, h_flags = SpecialSections.get(symbol.section)
        elf_section.header.sh_type = h_type
        elf_section.header.sh_flags = h_flags
        
        if symbol.section == ".text":
            def add_relocation(offset: int, addend: int, target: int, is_absolute: bool) -> None:
                name = symbols[target].elf_symbol.name
                elf_symbol = ElfSymbol(name)

                symbol_idx = elf_symbol_table.add_symbol(elf_symbol)

                reloc = ElfRela(offset, symbol_idx, ARM_RELOC_TYPE.R_ARM_ABS32 if is_absolute else ARM_RELOC_TYPE.R_ARM_JUMP24, addend)
                elf_relocs.add_reloc(reloc)
                array = bytearray(elf_section.data)
                if not is_absolute:
                    array[offset:offset+3] = (-2).to_bytes(3, byteorder="little", signed=True)
                elf_section.data = bytes(array)
            
            i = 0

            for insn in md.disasm(split_bytes, start):
                i += 1

                if insn.id == 0: # data
                    continue
                
                if insn.group(capstone.arm.ARM_GRP_JUMP) and not (insn.mnemonic == "bl" or insn.mnemonic == "blx"):
                    operand = insn.operands[0]
                    if operand.reg == capstone.arm.ARM_REG_LR:
                        add_mapping(insn.address - start + 4, "$d")
                    
                    if insn.cc in [capstone.arm.ARM_CC_AL, capstone.arm.ARM_CC_INVALID]:
                        add_mapping(insn.address - start + 4, "$d")
                    
                    if operand.type == capstone.arm.ARM_OP_IMM:
                        if operand.imm < current_func or operand.imm > next_func:
                            pass
                        else:
                            add_mapping(operand.imm - start, symbol.mapping)
        
        current_mapping = None
        for offset, mapping in mappings.items():
            if current_mapping != mapping:
                current_mapping = mapping
                mapping_symbol = ElfSymbol(mapping, offset, 0, st_shndx=section_idx)
                elf_symbol_table.add_symbol(mapping_symbol)
        
        elf.add_section(elf_section)
        section_idx += 1

        if symbol.section == ".text":
            elf.add_section(elf_relocs)
            section_idx += 1

    elf_bytes = bytes(elf)
    Path('split').mkdir(exist_ok=True)
    obj = 'split' / Path(split.file_name).with_suffix(".o")
    obj.parent.mkdir(exist_ok=True)
    obj.write_bytes(elf_bytes)
    
