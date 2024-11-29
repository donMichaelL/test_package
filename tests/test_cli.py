from unittest.mock import patch

import pytest
from click.testing import CliRunner

from theTrial.cli import init_command
from theTrial.utils import file_utils


@pytest.fixture(scope="module")
def runner():
    """Fixture that provides a Click CLI runner."""
    return CliRunner()


class TestInitCommand:
    """Test suite for the init_command CLI function."""

    @patch("theTrial.utils.cli_utils.create_file", return_value="OK")
    def test_create_file_called_with_default_name(self, mock_create_file, runner):
        """Test that the create_file function is called with default arguments"""
        runner.invoke(init_command)

        mock_create_file.assert_called_once_with(path=".", filename="app.py", content=file_utils.DEFAULT_APP_CONTENT)

    @patch("theTrial.utils.cli_utils.create_file", return_value="OK")
    def test_create_file_called_with_correct_arguments(self, mock_create_file, runner):
        """Test that the create_file function is called with the correct arguments."""
        runner.invoke(init_command, ["--name", "test_app"])

        mock_create_file.assert_called_once_with(
            path=".", filename="test_app.py", content=file_utils.DEFAULT_APP_CONTENT
        )

    @patch("theTrial.utils.cli_utils.create_file", return_value="OK")
    def test_success_message_displayed(self, mock_create_file, runner):
        """Test that the success message is displayed when a file is successfully created."""
        result = runner.invoke(init_command, ["--name", "test_app"])

        assert result.exit_code == 0
        assert "✅  Successfully created 'test_app.py' with the default app structure." in result.output


# class TestStartCommand:
#     def test_start_default(self, runner):
#         """Test the start command with the default name."""
#         result = runner.invoke(main, ["start"])
#         assert result.exit_code == 0
#     def test_start_custom_name(self, runner):
#         """Test the start command with a custom name."""
#         custon_name = "custom_app"
#         result = runner.invoke(main, ["start", "--name", custon_name])
#         assert result.exit_code == 0
# class TestRunCommand:
#     def test_run_default(self, runner):
#         """Test the run command without verbose."""
#         result = runner.invoke(main, ["run"])
#         assert result.exit_code == 0
#     def test_run_verbose(self, runner):
#         """Test the run command with verbose flag."""
#         result = runner.invoke(main, ["run", "--verbose"])
#         assert result.exit_code == 0
