from pathlib import Path


class FileUtils:

    files: list[Path] = []
    # fmt: off
    extensions: list[str] = [
        ".tex", ".txt", ".md",
        ".svg", ".gif", ".webp",
        ".pptx", ".ppt", ".pdf",
        ".mp3", ".m4a", ".wav",
        ".mkv", ".aep", ".mp4",
        ".m4v",".mov",
        ".jpeg", ".jpg", ".png",
        ".doc", ".docx", ".odt",
    ]
    # fmt: on
    root_dir: Path

    def __init__(self, path: Path) -> None:
        self.root_dir = path

    def get_all_files(self, path: Path) -> None:
        try:
            for item in path.iterdir():
                if item.is_file():
                    if item.suffix in self.extensions:
                        self.files.append(item)
                else:
                    self.get_all_files(item)
        except NotADirectoryError as e:
            print(f"Skipping: current item is not a directory. {e}")
        except FileNotFoundError as e:
            print(f"Skipping: current item is inaccessible. {e}")


if __name__ == "__main__":
    fileutils = FileUtils(Path.cwd())
    fileutils.get_all_files(fileutils.root_dir)

    with open("files.txt", "w") as f:
        f.write(str(fileutils.files))
