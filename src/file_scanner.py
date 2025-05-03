#  _   _  _____     ____  __ ____ _____ ____
# | \ | |/ _ \ \   / /  \/  | __ )___ /|  _ \
# |  \| | | | \ \ / /| |\/| |  _ \ |_ \| |_) |
# | |\  | |_| |\ V / | |  | | |_) |__) |  _ <
# |_| \_|\___/  \_/  |_|  |_|____/____/|_| \_\
#
# MIT License
#
# Copyright (c) 2024 Daniel Lima
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Module for recursively scanning files."""

from pathlib import Path

# fmt: off
TARGET_FILES: set[str] = {
    # Text & Documents
    ".txt", ".md", ".tex", ".pdf",
    ".doc", ".docx", ".odt", ".rtf",
    ".xls", ".xlsx", ".csv", ".tsv",
    ".ods",".ppt", ".pptx", ".odp",

    # Images & Graphics
    ".jpeg", ".jpg", ".png", ".gif", ".webp", ".bmp",
    ".tiff", ".svg", ".psd", ".ai", ".eps",

    # Audio
    ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac",

    # Video
    ".mp4", ".mkv", ".mov", ".avi", ".wmv", 
    ".m4v", ".flv", ".webm",

    # Project / Editable files
    ".aep", ".prproj", ".blend", ".sketch", 
    ".xd", ".fig", ".aup3", ".als",

    # Archives & Compressed
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2",

    # Code / Dev files
    ".py", ".java", ".js", ".ts", ".html", ".css", 
    ".json", ".xml", ".yml", ".yaml", ".c", ".cpp",
    ".h", ".hpp", ".rs", ".go", ".sh", ".bat", ".sql",

    # Configs and envs
    ".env", ".ini", ".cfg", ".toml", ".log",

    # Misc
    ".apk", ".exe", ".iso", ".dmg", ".db",
}

IGNORE_DIRS: set[str] = {
    ".git",          # Git metadata
    ".hg",           # Mercurial
    ".svn",          # Subversion
    "__pycache__",   # Python bytecode cache
    ".mypy_cache",   # mypy type check cache
    ".pytest_cache", # pytest cache
    ".venv", "venv", # virtual environments
    "env",           # common env dir
    "node_modules",  # JS dependencies
    "dist", "build", # build outputs
    ".idea",         # JetBrains IDE configs
    ".vscode",       # VSCode configs
    ".tox",          # tox envs
    ".cache",        # pip/npm cache
    ".next",         # Next.js build dir
    ".parcel-cache", # Parcel bundler
    "site-packages", # installed Python packages
}
# fmt: on


def get_all_files(
    path: Path,
    extensions: set[str] = TARGET_FILES,
    ignore_dirs: set[str] = IGNORE_DIRS,
) -> list[Path]:
    """
    Recursively collects all files within a directory (and its subdirectories)
    that match a given set of file extensions, while skipping ignored directories.

    Args:
        path (Path): The root directory from which to begin the search.
        extensions (set[str], optional): A set of file extensions (including the dot,
            e.g., ".txt", ".pdf") to include in the results. Defaults to TARGET_FILES.
        ignore_dirs (set[str], optional): A set of directory names to skip during traversal.
            The match is case-insensitive and applies to any folder in the path.
            Defaults to IGNORE_DIRS.

    Returns:
        list[Path]: A list of Path objects corresponding to files that match the criteria.
    """
    files: list[Path] = []

    try:
        for item in path.iterdir():
            if item.is_dir():
                if item.name in ignore_dirs:
                    continue
                files.extend(get_all_files(item, extensions, ignore_dirs))
            elif item.is_file() and item.suffix.lower() in extensions:
                files.append(item)

    except PermissionError:
        print(f"Skipping {path}: permission denied.")
    except (NotADirectoryError, FileNotFoundError):
        print(f"Skipping {path}: invalid file.")

    return files
