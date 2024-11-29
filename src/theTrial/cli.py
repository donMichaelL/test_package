import os
import sys

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .utils import cli_utils
from .utils import file_utils

__version__ = "2.0.1"


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script_path, run_app):
        self.script_path = script_path
        self.run_app = run_app

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            click.echo("[INFO] Detected changes, restarting application...")
            os.execv(sys.executable, [sys.executable] + sys.argv)  # nosec


@click.command("run", short_help="Run the application.")
@click.option("--app", default="app.py", show_default=True, help="The entry point of the application.")
@click.option("--reload", is_flag=True, help="Reload the application on code changes.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging.")
def run_command(app, reload, verbose):
    """Run the application."""

    click.echo(f"theTrial version v{__version__}")

    def extra_message(message):
        """Helper function for verbose logging."""
        if verbose:
            click.echo(message)

    def run_app():
        script_path = cli_utils.check_script_existence(app)
        click.echo(f"Entry point: {script_path}")
        app_instance = cli_utils.import_user_app(script_path)
        click.echo("The application is ready.")
        click.echo("Quit with CONTROL-C.\n")
        app_instance.run()

    if reload:
        script_path = cli_utils.check_script_existence(app)
        event_handler = ChangeHandler(script_path, run_app)
        observer = Observer()
        observer.schedule(
            event_handler,
            path=os.path.dirname(script_path) or ".",
            recursive=True,
        )
        observer.start()
        click.echo("[INFO] Watching for file changes...")

        try:
            run_app()
            observer.join()
        except KeyboardInterrupt:
            click.echo("[INFO] Stopping the watcher...")
            observer.stop()
        observer.join()

    else:
        run_app()


@click.command("init", short_help="Initialize your application.")
@click.option("--name", default="app", show_default=True, help="Name of the application.")
def init_command(name: str) -> None:
    """Initialize a new project structure."""
    click.echo(f"🚀  Initialize {name} project.")
    filename = f"{name}.py"
    cli_utils.create_file(path=".", filename=filename, content=file_utils.DEFAULT_APP_CONTENT)
    click.secho(f"✅  Successfully created '{filename}' with the default app structure.")
    click.secho("\nNext Steps:", bold=True)
    click.secho(f"  - Edit '{filename}' to customize your application.")
    click.secho("  - Run your app with theTrial run command.\n")
    click.secho("🎉  Happy Coding!", bold=True)


@click.group(help=f"theTrial CLI Tool v{__version__}")
@click.version_option(version=__version__, prog_name="theTrial")
def main():
    pass


main.add_command(init_command)
main.add_command(run_command)
