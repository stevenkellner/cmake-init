import re
import subprocess
import sys
from typing import Optional, Tuple


def determine_git_version() -> Optional[Tuple[int, int, int]]:
    process_output = subprocess.run("git --version", shell=True, capture_output=True)
    if process_output.returncode != 0:
        return None
    git_version_value = str(process_output.stdout, sys.stdout.encoding)
    git_version_match = re.search(r"\d+(\.\d+)+", git_version_value)
    if not git_version_match:
        return None
    git_version_str = git_version_match.group(0)
    git_version = list(map(int, git_version_str.rstrip().split(".")))
    if len(git_version) < 3:
        git_version += [0] * (3 - len(git_version))
    return git_version[0], git_version[1], git_version[2]


def init_git(path: str):
    git_version = determine_git_version()
    if git_version is None:
        print("\nGit can't be found! Can't initialize git for the project.\n")
        return
    branch = ""
    if (2, 28, 0) <= git_version:
        branch = " -b main"
    subprocess.run(f"git init{branch}", shell=True, check=True, cwd=path)
