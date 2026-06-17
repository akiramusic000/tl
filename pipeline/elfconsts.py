# ELF constants
# Taken from https://github.com/NSMBW-Community/NSMBW-Decomp.

import re
from enum import IntEnum, IntFlag

class ET(IntEnum):
    ET_NONE = 0
    ET_REL = 1
    ET_EXEC = 2
    ET_DYN = 3
    ET_CORE = 4


class EM(IntEnum):
    EM_NONE = 0
    EM_M32 = 1
    EM_SPARC = 2
    EM_386 = 3
    EM_68K = 4
    EM_88K = 5
    EM_860 = 7
    EM_MIPS = 8
    EM_S370 = 9
    EM_MIPS_RS3_LE = 10
    EM_PARISC = 15
    EM_VPP500 = 17
    EM_SPARC32PLUS = 18
    EM_960 = 19
    EM_PPC = 20
    EM_PPC64 = 21
    EM_S390 = 22
    EM_V800 = 36
    EM_FR20 = 37
    EM_RH32 = 38
    EM_RCE = 39
    EM_ARM = 40
    EM_ALPHA = 41
    EM_SH = 42
    EM_SPARCV9 = 43
    EM_TRICORE = 44
    EM_ARC = 45
    EM_H8_300 = 46
    EM_H8_300H = 47
    EM_H8S = 48
    EM_H8_500 = 49
    EM_IA_64 = 50
    EM_MIPS_X = 51
    EM_COLDFIRE = 52
    EM_68HC12 = 53
    EM_MMA = 54
    EM_PCP = 55
    EM_NCPU = 56
    EM_NDR1 = 57
    EM_STARCORE = 58
    EM_ME16 = 59
    EM_ST100 = 60
    EM_TINYJ = 61
    EM_X86_64 = 62
    EM_PDSP = 63
    EM_PDP10 = 64
    EM_PDP11 = 65
    EM_FX66 = 66
    EM_ST9PLUS = 67
    EM_ST7 = 68
    EM_68HC16 = 69
    EM_68HC11 = 70
    EM_68HC08 = 71
    EM_68HC05 = 72
    EM_SVX = 73
    EM_ST19 = 74
    EM_VAX = 75
    EM_CRIS = 76
    EM_JAVELIN = 77
    EM_FIREPATH = 78
    EM_ZSP = 79
    EM_MMIX = 80
    EM_HUANY = 81
    EM_PRISM = 82
    EM_AVR = 83
    EM_FR30 = 84
    EM_D10V = 85
    EM_D30V = 86
    EM_V850 = 87
    EM_M32R = 88
    EM_MN10300 = 89
    EM_MN10200 = 90
    EM_PJ = 91
    EM_OPENRISC = 92
    EM_ARC_A5 = 93
    EM_XTENSA = 94
    EM_VIDEOCORE = 95
    EM_TMM_GPP = 96
    EM_NS32K = 97
    EM_TPC = 98
    EM_SNP1K = 99
    EM_ST200 = 100


class SHN(IntEnum):
    SHN_UNDEF = 0
    SHN_LORESERVE = 0xff00
    SHN_LOPROC = 0xff00
    SHN_HIPROC = 0xff1f
    SHN_LOOS = 0xff20
    SHN_HIOS = 0xff3f
    SHN_ABS = 0xfff1
    SHN_COMMON = 0xfff2
    SHN_XINDEX = 0xffff
    SHN_HIRESERVE = 0xffff


class SHT(IntEnum):
    SHT_NULL = 0
    SHT_PROGBITS = 1
    SHT_SYMTAB = 2
    SHT_STRTAB = 3
    SHT_RELA = 4
    SHT_HASH = 5
    SHT_DYNAMIC = 6
    SHT_NOTE = 7
    SHT_NOBITS = 8
    SHT_REL = 9
    SHT_SHLIB = 10
    SHT_DYNSYM = 11
    SHT_INIT_ARRAY = 14
    SHT_FINI_ARRAY = 15
    SHT_PREINIT_ARRAY = 16
    SHT_GROUP = 17
    SHT_SYMTAB_SHNDX = 18
    SHT_LOOS = 0x60000000
    SHT_HIOS = 0x6fffffff
    SHT_LOPROC = 0x70000000
    SHT_HIPROC = 0x7fffffff
    SHT_LOUSER = 0x80000000
    SHT_MW_CATS = 0xca2a82c2
    SHT_HIUSER = 0xffffffff


class SHF(IntFlag):
    SHF_NONE = 0x0
    SHF_WRITE = 0x1
    SHF_ALLOC = 0x2
    SHF_EXECINSTR = 0x4
    SHF_MERGE = 0x10
    SHF_STRINGS = 0x20
    SHF_INFO_LINK = 0x40
    SHF_LINK_ORDER = 0x80
    SHF_OS_NONCONFORMING = 0x100
    SHF_GROUP = 0x200
    SHF_TLS = 0x400


class STB(IntEnum):
    STB_LOCAL = 0
    STB_GLOBAL = 1
    STB_WEAK = 2
    STB_LOOS = 10
    STB_HIOS = 12
    STB_LOPROC = 13
    STB_HIPROC = 15


class STT(IntEnum):
    STT_NOTYPE = 0
    STT_OBJECT = 1
    STT_FUNC = 2
    STT_SECTION = 3
    STT_FILE = 4
    STT_COMMON = 5
    STT_TLS = 6
    STT_LOOS = 10
    STT_HIOS = 12
    STT_LOPROC = 13
    STT_HIPROC = 15


class STV(IntEnum):
    STV_DEFAULT = 0
    STV_INTERNAL = 1
    STV_HIDDEN = 2
    STV_PROTECTED = 3


class STN(IntEnum):
    STN_UNDEF = 0


REL_SYM = re.compile(r'R_([0-9a-fA-F]+)_([0-9a-fA-F]+)_([0-9a-fA-F]+)')


class ARM_RELOC_TYPE(IntEnum):
    R_ARM_NONE = 0
    R_ARM_PC24 = 1
    R_ARM_ABS32 = 2
    R_ARM_REL32 = 3
    R_ARM_PC13 = 4
    R_ARM_ABS16 = 5
    R_ARM_ABS12 = 6
    R_ARM_THM_ABS5 = 7
    R_ARM_ABS8 = 8
    R_ARM_SBREL32 = 9
    R_ARM_THM_PC22 = 10
    R_ARM_THM_PC8 = 11
    R_ARM_AMP_VCALL9 = 12
    R_ARM_SWI24 = 13
    R_ARM_THM_SWI8 = 14
    R_ARM_XPC25 = 15
    R_ARM_THM_XPC22 = 16
    R_ARM_TLS_DTPMOD32 = 17
    R_ARM_TLS_DTPOFF32 = 18
    R_ARM_TLS_TPOFF32 = 19
    R_ARM_COPY = 20
    R_ARM_GLOB_DAT = 21
    R_ARM_JUMP_SLOT = 22
    R_ARM_RELATIVE = 23
    R_ARM_GOTOFF32 = 24
    R_ARM_BASE_PREL = 25
    R_ARM_GOT_BREL = 26
    R_ARM_PLT32 = 27
    R_ARM_CALL = 28
    R_ARM_JUMP24 = 29
    R_ARM_THM_JUMP24 = 30
    R_ARM_BASE_ABS = 31
    R_ARM_ALU_PCREL_7_0 = 32
    R_ARM_ALU_PCREL_15_8 = 33
    R_ARM_ALU_PCREL_23_15 = 34
    R_ARM_LDR_SBREL_11_0_NC = 35
    R_ARM_ALU_SBREL_19_12_NC = 36
    R_ARM_ALU_SBREL_27_20_CK = 37
    R_ARM_TARGET1 = 38
    R_ARM_SBREL31 = 39
    R_ARM_V4BX = 40
    R_ARM_TARGET2 = 41
    R_ARM_PREL31 = 42
    R_ARM_MOVW_ABS_NC = 43
    R_ARM_MOVT_ABS = 44
    R_ARM_MOVW_PREL_NC = 45
    R_ARM_MOVT_PREL = 46
    R_ARM_THM_MOVW_ABS_NC = 47
    R_ARM_THM_MOVT_ABS = 48
    R_ARM_THM_MOVW_PREL_NC = 49
    R_ARM_THM_MOVT_PREL = 50
    R_ARM_THM_JUMP19 = 51
    R_ARM_THM_JUMP6 = 52
    R_ARM_THM_ALU_PREL_11_0 = 53
    R_ARM_THM_PC12 = 54
    R_ARM_ABS32_NOI = 55
    R_ARM_REL32_NOI = 56
    R_ARM_ALU_PC_G0_NC = 57
    R_ARM_ALU_PC_G0 = 58
    R_ARM_ALU_PC_G1_NC = 59
    R_ARM_ALU_PC_G1 = 60
    R_ARM_ALU_PC_G2 = 61
    R_ARM_LDR_PC_G1 = 62
    R_ARM_LDR_PC_G2 = 63
    R_ARM_LDRS_PC_G0 = 64
    R_ARM_LDRS_PC_G1 = 65
    R_ARM_LDRS_PC_G2 = 66
    R_ARM_LDC_PC_G0 = 67
    R_ARM_LDC_PC_G1 = 68
    R_ARM_LDC_PC_G2 = 69
    R_ARM_ALU_SB_G0_NC = 70
    R_ARM_ALU_SB_G0 = 71
    R_ARM_ALU_SB_G1_NC = 72
    R_ARM_ALU_SB_G1 = 73
    R_ARM_ALU_SB_G2 = 74
    R_ARM_LDR_SB_G0 = 75
    R_ARM_LDR_SB_G1 = 76
    R_ARM_LDR_SB_G2 = 77
    R_ARM_LDRS_SB_G0 = 78
    R_ARM_LDRS_SB_G1 = 79
    R_ARM_LDRS_SB_G2 = 80
    R_ARM_LDC_SB_G0 = 81
    R_ARM_LDC_SB_G1 = 82
    R_ARM_LDC_SB_G2 = 83
    R_ARM_MOVW_BREL_NC = 84
    R_ARM_MOVT_BREL = 85
    R_ARM_MOVW_BREL = 86
    R_ARM_THM_MOVW_BREL_NC = 87
    R_ARM_THM_MOVT_BREL = 88
    R_ARM_THM_MOVW_BREL = 89
    R_ARM_TLS_GOTDESC = 90
    R_ARM_TLS_CALL = 91
    R_ARM_TLS_DESCSEQ = 92
    R_ARM_THM_TLS_CALL = 93
    R_ARM_PLT32_ABS = 94
    R_ARM_GOT_ABS = 95
    R_ARM_GOT_PREL = 96
    R_ARM_GOT_BREL12 = 97
    R_ARM_GOTOFF12 = 98
    R_ARM_GOTRELAX = 99
    R_ARM_GNU_VTENTRY = 100
    R_ARM_GNU_VTINHERIT = 101
    R_ARM_THM_JUMP11 = 102
    R_ARM_THM_JUMP8 = 103
    R_ARM_TLS_GD32 = 104
    R_ARM_TLS_LDM32 = 105
    R_ARM_TLS_LDO32 = 106
    R_ARM_TLS_IE32 = 107
    R_ARM_TLS_LE32 = 108
    R_ARM_TLS_LDO12 = 109
    R_ARM_TLS_LE12 = 110
    R_ARM_TLS_IE12GP = 111
    R_ARM_ME_TOO = 128
    R_ARM_THM_TLS_DESCSEQ16 = 129
    R_ARM_THM_TLS_DESCSEQ32 = 130
    R_ARM_THM_GOT_BREL12 = 131
    R_ARM_THM_ALU_ABS_G0_NC = 132
    R_ARM_THM_ALU_ABS_G1_NC = 133
    R_ARM_THM_ALU_ABS_G2_NC = 134
    R_ARM_THM_ALU_ABS_G3 = 135
    R_ARM_THM_BF16 = 136
    R_ARM_THM_BF12 = 137
    R_ARM_THM_BF18 = 138


class SpecialSections:

    _lookup: dict[str, tuple[SHT, SHF]] = {
        'extab_': (SHT.SHT_PROGBITS, SHF.SHF_ALLOC),
        'extabindex_': (SHT.SHT_PROGBITS, SHF.SHF_ALLOC),
        '.bss': (SHT.SHT_NOBITS, SHF.SHF_ALLOC | SHF.SHF_WRITE),
        '.comment': (SHT.SHT_PROGBITS, SHF.SHF_NONE),
        '.ctors': (SHT.SHT_PROGBITS, SHF.SHF_ALLOC),
        '.data': (SHT.SHT_PROGBITS, SHF.SHF_ALLOC | SHF.SHF_WRITE),
        '.dtors': (SHT.SHT_PROGBITS, SHF.SHF_ALLOC),
        '.init': (SHT.SHT_PROGBITS, SHF.SHF_ALLOC | SHF.SHF_EXECINSTR),
        '.rodata': (SHT.SHT_PROGBITS, SHF.SHF_ALLOC),
        '.sbss': (SHT.SHT_NOBITS, SHF.SHF_ALLOC | SHF.SHF_WRITE),
        '.sbss2': (SHT.SHT_NOBITS, SHF.SHF_ALLOC | SHF.SHF_WRITE),
        '.sdata': (SHT.SHT_PROGBITS, SHF.SHF_ALLOC | SHF.SHF_WRITE),
        '.sdata2': (SHT.SHT_PROGBITS, SHF.SHF_ALLOC | SHF.SHF_WRITE),
        '.shstrtab': (SHT.SHT_STRTAB, SHF.SHF_NONE),
        '.strtab': (SHT.SHT_STRTAB, SHF.SHF_NONE),
        '.symtab': (SHT.SHT_SYMTAB, SHF.SHF_NONE),
        '.text': (SHT.SHT_PROGBITS, SHF.SHF_ALLOC | SHF.SHF_EXECINSTR)
    }

    @staticmethod
    def get(sec_name: str) -> tuple[SHT, SHF]:
        if sec_name in SpecialSections._lookup:
            return SpecialSections._lookup[sec_name]
        if sec_name.startswith('.rel.'):
            return (SHT.SHT_REL, SHF.SHF_NONE)
        if sec_name.startswith('.rela.'):
            return (SHT.SHT_RELA, SHF.SHF_NONE)
        return (SHT.SHT_NULL, SHF.SHF_NONE)