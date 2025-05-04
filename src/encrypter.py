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

import sys
from anyio import open_file
from anyio import Path as aPath
from io import DEFAULT_BUFFER_SIZE
from cryptography.fernet import Fernet


class Encrypter:

    def __init__(self, fernet: Fernet) -> None:
        self.__fernet = fernet

    @staticmethod
    def gen_key() -> bytes:
        return Fernet.generate_key()

    @staticmethod
    def get_fernet(key: str | bytes) -> Fernet:
        if isinstance(key, str):
            key = key.encode()
        return Fernet(key)

    @classmethod
    def from_key(cls, key: str | bytes) -> "Encrypter":
        if isinstance(key, str):
            key = key.encode()
        return cls(Fernet(key))

    async def parse_files(self, files: list[aPath], decrypt: bool = False) -> None:
        if not decrypt:
            for _file in files:
                await self.encrypt_file(_file)
        else:
            for _file in files:
                await self.decrypt_file(_file)

    async def encrypt_file(self, path: aPath, buff: int = DEFAULT_BUFFER_SIZE) -> None:
        temp_f = path.with_name(path.suffix + ".temp")
        # fmt: off
        async with await open_file(path, "rb") as f_in, await open_file(temp_f, "wb") as f_out:
            # fmt: on
            try:
                while True:
                    chunk = await f_in.read(buff)
                    if not chunk:
                        break
                    encrypted = self.__fernet.encrypt(chunk)
                    await f_out.write(len(encrypted).to_bytes(4, sys.byteorder)) # 32 bits integer
                    await f_out.write(encrypted)
                await temp_f.replace(path)
            except (PermissionError, FileNotFoundError, IsADirectoryError) as e:
                print(f"Skipping: {path}: {e}")

    async def decrypt_file(self, path: aPath) -> None:
        temp_f = path.with_name(path.suffix + ".temp")
        # fmt: off
        async with await open_file(path, "rb") as f_in, await open_file(temp_f, "wb") as f_out:
            # fmt: on
            try:
                while True:
                    size_bytes = await f_in.read(4)
                    if not size_bytes:
                        break

                    size = int.from_bytes(size_bytes)
                    encrypted_chunk = await f_in.read(size)
                    if len(encrypted_chunk) != size:
                        raise ValueError(f"Corrupted File: expected {size} bytes, got {len(encrypted_chunk)}")

                    plain_chunk = self.__fernet.decrypt(encrypted_chunk)
                    await f_out.write(len(plain_chunk).to_bytes(4, sys.byteorder)) # 32 bits integer
                    await f_out.write(plain_chunk)
                await temp_f.replace(path)
            except (PermissionError, FileNotFoundError, IsADirectoryError, ValueError) as e:
                print(f"Skipping: {path}: {e}")
