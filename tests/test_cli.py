import pytest
from click.testing import CliRunner

from theTrial.cli import main


@pytest.fixture
def runner():
    """Fixture that provides a Click CLI runner."""
    return CliRunner()


class TestStartCommand:
    def test_start_default(self, runner):
        """Test the start command with the default name."""
        result = runner.invoke(main, ["start"])
        assert result.exit_code == 0
        assert "[INFO] app files are created." in result.output

    def test_start_custom_name(self, runner):
        """Test the start command with a custom name."""
        custon_name = "custom_app"
        result = runner.invoke(main, ["start", "--name", custon_name])
        assert result.exit_code == 0
        assert f"[INFO] {custon_name} files are created." in result.output


class TestRunCommand:
    def test_run_default(self, runner):
        """Test the run command without verbose."""
        result = runner.invoke(main, ["run"])
        assert result.exit_code == 0

    def test_run_verbose(self, runner):
        """Test the run command with verbose flag."""
        result = runner.invoke(main, ["run", "--verbose"])
        assert result.exit_code == 0
