from pipeline.ninja_syntax_ex import Writer
from pathlib import Path
from dataclasses import dataclass
import json
import os

@dataclass
class Lib:
    name: str
    cflags: list[str]
    sources: list[tuple[bool, Path]]

type Libs = list[Lib]

def write_ninja(libs: Libs):
    if os.name == "nt":
        exe = ".exe"
    else:
        exe = ""

    writer = Writer()
    writer.variable("cc", f"tools/armcc/armcc.exe")
    writer.variable("ld", f"tools/binutils/arm-none-eabi-ld{exe}")
    writer.newline()

    writer.rule("cc", "python3 pipeline/armcc.py $cc $in -o $out -c $ccflags", description = "CC $in")
    writer.rule("ld", "$ld $in -o $out", description = "Linking $out")
    writer.newline()

    sources: list[tuple[bool, Path, list[str]]] = []
    for lib in libs:
        sources += [(source[0], source[1], lib.cflags) for source in lib.sources]
    
    objects = ["build" / source[1].with_suffix(".o").relative_to("src/") for source in sources]

    commands = []
    objdiff = {
        "build_target": False,
        "custom_make": "ninja",
        "watch_patterns": [
            "*.c",
            "*.cc",
            "*.cp",
            "*.cpp",
            "*.cxx",
            "*.c++",
            "*.h",
            "*.hh",
            "*.hp",
            "*.hpp",
            "*.hxx",
            "*.h++",
            "*.pch",
            "*.pch++",
            "*.inc",
            "*.py",
            "*.yml",
            "*.txt",
            "*.json"
        ],
        "units": []
    }
    units = []
    for ((_, path, cflags), object) in zip(sources, objects):
        writer.build("cc", object, inputs=[path], ccflags=" ".join(cflags))

        command = {
            'directory': str(Path.cwd()),
            'file': str(path),
            'output': str(object),
            'arguments': ["/usr/bin/clang", "-o", str(object), "-c", str(path)],
        }
        commands.append(command)

        unit = {
            "name": str(path.with_suffix("")),
            "target_path": str('split' / object.relative_to("build/")),
            "base_path": str(object),
        }
        units.append(unit)

    writer.newline()

    writer.rule("configure", "python3 configure.py")
    writer.build("configure", "phony", implicit_inputs=["configure.py"])

    writer.flush("build.ninja")

    Path('compile_commands.json').write_text(json.dumps(commands, indent=2))
    objdiff["units"] = units
    Path('objdiff.json').write_text(json.dumps(objdiff, indent=2))