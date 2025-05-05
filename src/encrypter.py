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
"""Provides functionality to encrypt and decrypt files using Fernet symmetric encryption."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from io import DEFAULT_BUFFER_SIZE
import os
from pathlib import Path
import sys

from cryptography.fernet import Fernet

MAX_WORKERS = min(32, (os.cpu_count() or 1) * 4)


def encrypt_stream(
    fernet: Fernet, file: Path, suffix: str = ".locked", buff: int = DEFAULT_BUFFER_SIZE
) -> None:
    """Encrypts a file stream and saves it with a new name.

    Args:
        fernet (Fernet): The Fernet instance used for encryption.
        file (Path): The file path to be encrypted.
        suffix (str, optional): The suffix to be added to the encrypted file's name. Defaults to ".locked".
        buff (int, optional): The buffer size for reading chunks of the file. Defaults to DEFAULT_BUFFER_SIZE.
    """
    enc_file = file.parent / (file.name + suffix)
    try:
        with open(file, "rb") as f_in, open(enc_file, "wb") as f_out:
            while True:
                chunk = f_in.read(buff)
                if not chunk:
                    break  # EOF
                enc = fernet.encrypt(chunk)
                f_out.write(len(enc).to_bytes(4, sys.byteorder))
                f_out.write(enc)
        file.unlink()
    except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
        print(f"Skipping: {file}: {e}")


def decrypt_stream(fernet: Fernet, file: Path) -> None:
    """Decrypts an encrypted file stream.

    Args:
        fernet (Fernet): The Fernet instance used for decryption.
        file (Path): The encrypted file path to be decrypted.

    Raises:
        ValueError: If the encrypted file is corrupted.
    """
    decp_file = file.with_name(file.name.removesuffix(".locked"))
    try:
        with open(file, "rb") as f_in, open(decp_file, "wb") as f_out:
            while True:
                size_bytes = f_in.read(4)
                if not size_bytes:
                    break  # EOF

                size = int.from_bytes(size_bytes, sys.byteorder)
                enc_chunck = f_in.read(size)
                if len(enc_chunck) != size:
                    raise ValueError(
                        f"Corrupted File: expected {size} bytes, got {len(enc_chunck)}"
                    )

                plain_chunck = fernet.decrypt(enc_chunck)
                f_out.write(plain_chunck)
        file.unlink()
    except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
        print(f"Skipping: {file}: {e}")


def parse_files(fernet: Fernet, files: list[Path], decrypt: bool = False) -> None:
    """
    Encrypts or decrypts a list of files concurrently.

    Args:
        fernet (Fernet): The Fernet instance used for encryption or decryption.
        files (list[Path]): The list of file paths to be processed.
        decrypt (bool, optional): If True, the files will be decrypted. Defaults to False (encrypt).
    """
    handler = decrypt_stream if decrypt else encrypt_stream
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(handler, fernet, file) for file in files]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error: {e}")
