from pathlib import Path


def list_file_paths_in_dir(directory: str) -> list[str]:
    """
    Returns a list of absolute file paths from the specified directory.
    """
    d = Path(directory)
    if not d.exists():
        raise FileNotFoundError(f"Directory not found: {d}")

    return [str(file_path) for file_path in d.iterdir() if file_path.is_file()]
