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

import logging
from pathlib import Path


class FileUtils:

    # fmt: off
    extensions: list[str] = [
        ".tex", ".txt", ".md",
        ".svg", ".gif", ".webp",
        ".pptx", ".ppt", ".pdf",
        ".mp3", ".m4a", ".wav",
        ".mkv", ".aep", ".mp4",
        ".m4v",".mov",
        ".jpeg", ".jpg", ".png",
        ".doc", ".docx", ".odt",
    ]
    # fmt: on

    def __init__(self) -> None:
        self.files: list[Path] = []

    def get_all_files(self, path: Path) -> None:
        """
        Recursively collects file paths from the given directory and subdirectories
        that match allowed file extensions.
        
        Args:
            path (Path): The root directory path to start the file search.

        Raises:
            NotADirectoryError: If a path is expected to be a directory but is not.
            FileNotFoundError: If a file or directory cannot be accessed.
            PermissionError: If the program lacks the necessary permissions to access a file or directory.
        """
        try:
            for item in path.iterdir():
                if item.is_file() and item.suffix in self.extensions:
                    self.files.append(item)
                else:
                    self.get_all_files(item)

        except NotADirectoryError as e:
            logging.warning(f"Skipping: current item is not a directory. {e}")
        except FileNotFoundError as e:
            logging.warning(f"Skipping: current item is inaccessible. {e}")
        except PermissionError as e:
            logging.warning(f"Skipping: permission deined to access current item. {e}")


if __name__ == "__main__":
    fileutils = FileUtils()
    fileutils.get_all_files(Path.cwd())

    with open("files.txt", "w") as f:
        f.write(str(fileutils.files))
