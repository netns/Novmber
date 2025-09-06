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

__version__ = "1.0.0"

import sys
from getopt import GetoptError, getopt
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet

from decrypter import Decrypter
from encrypter import Encrypter
from file_scanner import get_all_files


def usage():
    banner = r"""
    _   _  _____     ____  __ ____ _____ ____  
    | \ | |/ _ \ \   / /  \/  | __ )___ /|  _ \ 
    |  \| | | | \ \ / /| |\/| |  _ \ |_ \| |_) |
    | |\  | |_| |\ V / | |  | | |_) |__) |  _ < 
    |_| \_|\___/  \_/  |_|  |_|____/____/|_| \_\

    Novmber - File Encryption & Decryption Tool
    """
    print(banner)
    print(f"Version: {__version__}\n")
    print("Usage:")
    print("  python main.py -e <path> -k <keyfile>   Encrypt file or directory")
    print("  python main.py -d <path> -k <keyfile>   Decrypt file or directory")
    print(
        "  python main.py -g [-k <keyfile>]        Generate key (print or save to file)"
    )
    print("  python main.py -h                       Show this help")
    print("  python main.py -v                       Show version")


def save_key(key: bytes, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(key)
    dest.chmod(0o600)


def load_key(dest: Path) -> bytes:
    if not dest.exists():
        raise ValueError("Path doesn't exists.")
    return dest.read_bytes()


def parse_args(argv: list[str] | None = None):
    if not argv:
        argv = sys.argv[1:]

    args_dict: dict[str, Any] = {
        "mode": None,  # encrypt, decrypt or gen-key
        "target": None,  # target directory or file
        "keyfile": None,  # key file path
    }

    try:
        opts, _ = getopt(
            argv,
            "e:d:gk:hv",
            ["encrypt=", "decrypt=", "gen-key", "key=", "help", "version"],
        )
    except GetoptError as e:
        print(f"Error: {e}")
        usage()
        sys.exit(1)

    for opt, val in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-v", "--version"):
            print(f"Novmber v{__version__}")
            sys.exit(0)
        elif opt in ("-e", "--encrypt"):
            if args_dict["mode"] is not None:
                print("Error: Can't use encrypt and decrypt at the same time.")
                sys.exit(1)
            args_dict["mode"] = "encrypt"
            args_dict["target"] = Path(val).expanduser().resolve()
        elif opt in ("-d", "--decrypt"):
            if args_dict["mode"] is not None:
                print("Error: Can't use encrypt and decrypt at the same time.")
                sys.exit(1)
            args_dict["mode"] = "decrypt"
            args_dict["target"] = Path(val).expanduser().resolve()
        elif opt in ("-g", "--gen-key"):
            args_dict["mode"] = "gen-key"
        elif opt in ("-k", "--key"):
            args_dict["keyfile"] = Path(val).expanduser().resolve()

    # Default values
    if args_dict["target"] is None and args_dict["mode"] in ("encrypt", "decrypt"):
        args_dict["target"] = Path(".").resolve()

    return args_dict


def encrypt_mode(key: bytes, dest: Path) -> None:
    frnt = Fernet(key)
    enc = Encrypter(frnt)
    if dest.is_file():
        enc.encrypt_file(dest)
    elif dest.is_dir():
        enc.files = get_all_files(dest)
        enc.encrypt()
    else:
        raise ValueError(f"Invalid target: {dest}")


def decrypt_mode(key: bytes, dest: Path) -> None:
    frnt = Fernet(key)
    enc = Decrypter(frnt)
    if dest.is_file():
        enc.decrypt_file(dest)
    elif dest.is_dir():
        enc.files = get_all_files(dest)
        enc.decrypt()
    else:
        raise ValueError(f"Invalid target: {dest}")


def main():
    args_dict = parse_args()

    match args_dict["mode"]:
        case "encrypt":
            if not args_dict["keyfile"]:
                print("Error: You must provide a key file for encryption.")
                sys.exit(1)
            if not args_dict["keyfile"].exists():
                key = Fernet.generate_key()
                save_key(key, args_dict["keyfile"])
            else:
                key = args_dict["keyfile"].read_bytes()
            encrypt_mode(key, args_dict["target"])

        case "decrypt":
            if not args_dict["keyfile"] or not args_dict["keyfile"].exists():
                print("Error: Key file is required for decryption.")
                sys.exit(1)
            key = load_key(args_dict["keyfile"])
            decrypt_mode(key, args_dict["target"])

        case "gen-key":
            key = Fernet.generate_key()
            if file := args_dict["keyfile"]:
                file.write_bytes(key)
            else:
                print(key.decode())

        case None:
            usage()
            sys.exit(1)

        case _:
            print("Error: Unknown mode.")
            usage()
            sys.exit(1)


if __name__ == "__main__":
    main()
