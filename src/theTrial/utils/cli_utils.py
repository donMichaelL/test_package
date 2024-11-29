import os


def create_file(path: str, filename: str, content: str = "") -> None:
    """Create a file with the specified content at the given path and filename."""
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, filename), "w") as file:
        file.write(content)
