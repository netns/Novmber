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

"""Provides functionality to decrypt files using Fernet symmetric encryption."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import Iterable, Literal

from cryptography.fernet import Fernet

from utils import MAX_WORKERS


class Decrypter:
    def __init__(
        self,
        fernet: Fernet,
        files: Iterable[Path] | None = None,
        byteorder: Literal["little", "big"] = "big",
    ):
        self.files = files
        self.fernet = fernet
        self.byteorder = byteorder

    def _decrypt_stream(self, input: BufferedReader, output: BufferedWriter):
        """
        Decrypts data from an input stream and writes it to an output stream in chunks.

        Reads each chunk's length from the first 4 bytes and decrypts it using Fernet.

        Args:
            input_stream (BufferedReader): Stream to read encrypted data from.
            output_stream (BufferedWriter): Stream to write decrypted data to.
        """
        while 1:
            size_bytes = input.read(4)
            if not size_bytes:
                break  # EOF

            size = int.from_bytes(size_bytes, self.byteorder)  # type: ignore
            chunk = input.read(size)
            if len(chunk) != size:
                raise ValueError(
                    f"Corrupted File: expected {size} bytes, got {len(chunk)}"
                )
            dec = self.fernet.decrypt(chunk)
            output.write(dec)

    def decrypt_file(self, file: Path):
        """
        Decrypts a single file and removes the ".locked" suffix.

        Args:
            file (Path): Path to the file to decrypt.
        """
        dest = file.with_name(file.name.removesuffix(".locked"))
        try:
            with file.open("rb") as f_in, dest.open("wb") as f_out:
                self._decrypt_stream(f_in, f_out)
        except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
            print(f"Skipping: {file}: {e}")

    def decrypt(self):
        """
        Decrypts all files provided to the Decrypter instance using a thread pool.

        Files are processed concurrently up to MAX_WORKERS threads. Raises ValueError
        if no files are provided. Exceptions during decryption are caught and logged
        without stopping the process.
        """
        if not self.files:
            raise ValueError("Files cannot be empty")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(self.decrypt_file, file) for file in self.files]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error: {e}")
