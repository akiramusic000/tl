from pathlib import Path
from pipeline.parse_splits import Split
from pipeline.elf import ElfSection, ElfFile, ElfSymbol, ElfSymtab, ElfRela, ElfRelaSec
from pipeline.elfconsts import ET, EM, ARM_RELOC_TYPE
import capstone
import os

def split(code_bin: Path, exheader: Path, split: Split, symbols: dict[int, tuple[ElfSymbol, str]]):
    symbol_addrs = list(symbols.keys())

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

    for (section, (start, end)) in split.sections.items():
        in_code = True
        current_func = start
        next_func = current_func + symbols[start][0].st_size

        if section == ".text":
            elf_relocs = ElfRelaSec('.rela.text')
            elf_relocs.header.sh_info = section_idx
            elf_relocs.header.sh_link = 1

        code_bin_file.seek(start - base_address, os.SEEK_SET)
        split_bytes = code_bin_file.read(end - start)
        elf_section = ElfSection(section, split_bytes)

        def add_mapping(offset: int, type: str):
            mapping_symbol = ElfSymbol(type, offset, 0, st_shndx=section_idx)
            elf_symbol_table.add_symbol(mapping_symbol)
        
        if section == ".text":
            def add_relocation(offset: int, addend: int, target: int, is_absolute: bool) -> None:
                name = symbols[target][0].name
                elf_symbol = ElfSymbol(name) # 00105444

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

                if insn.address in symbols.keys():
                    current_func = insn.address
                    next_func = current_func + symbols[start][0].st_size
                    in_code = True

                    symbol, mapping = symbols[insn.address]

                    symbol.st_shndx = section_idx

                    add_mapping(insn.address - start, mapping)
                    elf_symbol_table.syms.append(symbol)
                
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
                            add_mapping(operand.imm - start, "$a")

        
        elf.add_section(elf_section)
        section_idx += 1

        if section == ".text":
            elf.add_section(elf_relocs)
            section_idx += 1

    elf_bytes = bytes(elf)
    Path('split').mkdir(exist_ok=True)
    obj = 'split' / Path(split.file_name).with_suffix(".o")
    obj.parent.mkdir(exist_ok=True)
    obj.write_bytes(elf_bytes)
    
