import os


def scan_files(root_dir: str, suffix: str) -> list[str]:
    """Scan files with a certain suffix in the root directory

    Args:
        root_dir (str): root directory
        suffix (str): file suffix (extension) without "." in the beginning

    Returns:
        list[str]: file paths without file extension
    """
    return [
        root + "\\" + file.replace(f".{suffix}", "")
        for root, dirs, files in os.walk(root_dir)
        for file in files
        if file.endswith(f".{suffix}")
    ]