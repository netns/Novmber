#  _   _  _____     ____  __ ____ _____ ____
# | \ | |/ _ \ \   / /  \/  | __ )___ /|  _ \
# |  \| | | | \ \ / /| |\/| |  _ \ |_ \| |_) |
# | |\  | |_| |\ V / | |  | | |_) |__) |  _ <
# |_| \_|\___/  \_/  |_|  |_|____/____/|_| \_\
#
# Copyright (c) 2024-2025 Daniel Lima
#
# Licensed under the MIT License.
# See the LICENSE file in the project root for full license text.CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module for recursively scanning files."""

import os
from collections import deque
from pathlib import Path
from typing import Iterator

"""
Sets are used instead of lists/tuples for O(1) membership checks,
automatic uniqueness, and clearer semantics when filtering files/dirs.
"""

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
    root_path: Path,
    extensions: set[str] | None = None,
    ignore_dirs: set[str] | None = None,
) -> Iterator[Path]:
    """
    Lazily traverses a directory tree and yields files that match the given extensions,
    skipping any directories specified in the ignore list.

    This function performs a breadth-first search (BFS) using a deque, without following
    symbolic links. It yields results one by one, making it suitable for processing large
    directory trees without loading everything into memory.

    Args:
        root_path (Path): The root directory from which to begin the search.
        extensions (set[str], optional): A set of file extensions to include in the
            results (including the dot, e.g., ".txt", ".pdf"). Defaults to TARGET_FILES.
        ignore_dirs (set[str], optional): A set of directory names to skip during
            traversal. The comparison is case-sensitive. Defaults to IGNORE_DIRS.

    Yields:
        Path: The full path to each file that matches the given criteria.
    """
    extensions = extensions or TARGET_FILES
    ignore_dirs = ignore_dirs or IGNORE_DIRS

    stack = deque([root_path])

    while stack:
        current_path = stack.popleft()
        try:
            with os.scandir(current_path) as it:
                for entry in it:
                    if (
                        entry.is_dir(follow_symlinks=False)
                        and entry.name not in ignore_dirs
                    ):
                        stack.append(Path(entry.path))
                    elif (
                        entry.is_file(follow_symlinks=False)
                        and Path(entry.name).suffix.lower() in extensions
                    ):
                        yield Path(entry.path)

        except PermissionError:
            print(f"Skipping {current_path}: permission denied.")
        except (NotADirectoryError, FileNotFoundError):
            print(f"Skipping {current_path}: invalid file.")
