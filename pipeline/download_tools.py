import platform
from urllib.request import urlretrieve
import zipfile
from pathlib import Path
import stat

def download_binutils(tool_dir: Path):
    uname = platform.uname()
    system = uname.system.lower()
    arch = uname.machine.lower()
    if system == "darwin":
        system = "macos"
        arch = "universal"
    elif arch == "amd64":
        arch = "x86_64"
    binutils_url = f"https://github.com/akiramusic000/3ds-binutils/releases/download/2.42-0/{system}-{arch}.zip"

    path, _ = urlretrieve(binutils_url, tool_dir / "binutils.zip")
    with zipfile.ZipFile(path, "r") as zip:
        zip.extractall(tool_dir / "binutils")
    Path(path).unlink()

def download_armcc(tool_dir: Path):
    uname = platform.uname()
    system = uname.system.lower()
    arch = uname.machine.lower()
    if system == "darwin":
        system = "macos"
        arch = "universal"
    elif arch == "amd64":
        arch = "x86_64"
    armcc_url = f"https://github.com/decompme/compilers/releases/download/compilers/armcc.zip"

    path, _ = urlretrieve(armcc_url, tool_dir / "armcc.zip")
    with zipfile.ZipFile(path, "r") as zip:
        zip.extractall(tool_dir / "armcc")
    Path(path).unlink()

def download_wibo(tool_dir: Path):
    uname = platform.uname()
    system = uname.system.lower()
    arch = uname.machine.lower()
    name = arch
    if system == "darwin":
        name = "macos"
    elif arch == "amd64":
        name = "x86_64"
    wibo_url = f"https://github.com/decompals/wibo/releases/download/1.1.0/wibo-{name}"

    wibo_path = tool_dir / "wibo"
    path, _ = urlretrieve(wibo_url, wibo_path)
    wibo_path.chmod(wibo_path.stat().st_mode | stat.S_IEXEC)

def download_tools():
    tool_dir = Path("tools/")
    tool_dir.mkdir(exist_ok=True)

    if not (tool_dir / 'binutils').exists():
        download_binutils(tool_dir)
    if not (tool_dir / 'armcc').exists():
        download_armcc(tool_dir)

    uname = platform.uname()
    system = uname.system.lower()

    if system != "windows":
        if not (tool_dir / 'wibo').exists():
            download_wibo(tool_dir)
