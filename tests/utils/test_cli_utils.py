from theTrial.utils.cli_utils import create_file


def test_create_file(tmp_path):
    """Test that a file is created with the correct content at the specified path."""
    filename = "fake_file.txt"
    content = "fake_content"
    create_file(tmp_path, filename, content)

    file_path = tmp_path / filename
    assert tmp_path.exists()
    assert file_path.exists()
    assert file_path.read_text() == content


def test_create_file_in_nested_directory(tmp_path):
    """Test that a file is created with the correct content in a nested directory."""
    nested_path = tmp_path / "nested"
    filename = "nested_file.txt"
    content = "Nested content"
    create_file(path=nested_path, filename=filename, content=content)

    file_path = nested_path / filename
    assert file_path.exists()
    assert file_path.read_text() == content
