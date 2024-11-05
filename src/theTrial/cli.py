import importlib.util
import os
import sys

import click
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .exceptions import AppImportError
from .exceptions import ScriptPathError
from theTrial.app import TheTrial

__version__ = "2.0.1"


def get_script_path(app):
    script_path = app or os.getenv("THE_TRIAL_APP")

    if not script_path:
        raise ScriptPathError(
            "No script specified. Provide a script using --app option "
            "or set the environment variable 'THE_TRIAL_APP'."
        )
    if not os.path.exists(script_path):
        raise ScriptPathError(f"The script '{script_path}' does not exist.")

    return script_path


def get_module_spec(script_path):
    """Get the module specification for a given script path."""
    module_name = os.path.splitext(os.path.basename(script_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if not spec or not spec.loader:
        raise AppImportError(f"Cannot find a valid module specification for '{script_path}'.")
    return spec


def load_module_from_spec(spec):
    """Load a module from a given module spec."""
    user_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(user_module)
    except Exception as e:
        raise AppImportError(f"Failed to import module '{spec.name}' from '{spec.origin}': {e}")
    return user_module


def get_app_instance(user_module):
    """Retrieve and validate the 'app' object from the user-defined module."""
    if not hasattr(user_module, "app"):
        raise AppImportError("No 'app' instance found in the script. " "Make sure you define 'app = TheTrial()'.")

    app = getattr(user_module, "app")  # noqa: B009
    if not isinstance(app, TheTrial):
        raise AppImportError(f"The 'app' object in '{user_module.__name__}' " "is not an instance of TheTrial.")

    return app


def import_user_app(script_path):
    """
    Dynamically import the user-defined module and return the 'app' object
    if it exists.
    """
    script_dir = os.path.dirname(script_path)
    sys.path.insert(0, script_dir)

    spec = get_module_spec(script_path)
    user_module = load_module_from_spec(spec)
    return get_app_instance(user_module)


@click.command("init", short_help="Init your application.")
@click.option("--name", default="app", help="Name of the application.")
def init_command(name: str) -> None:
    """Initialize a new project structure."""
    click.echo(f"[INFO] Initialize {name} project.")


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script_path, run_app):
        self.script_path = script_path
        self.run_app = run_app

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            click.echo("[INFO] Detected changes, restarting application...")
            os.execv(sys.executable, [sys.executable] + sys.argv)  # nosec


@click.command("run", short_help="Run the application.")
@click.option(
    "--app",
    type=str,
    help="Specify the application script to run (e.g., --app dummy.py).",
)
@click.option("--reload", is_flag=True, help="Reload the application on code changes.")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging.")
def run_command(app, reload, verbose):
    """Run the application."""

    def extra_message(message):
        """Helper function for verbose logging."""
        if verbose:
            click.echo(message)

    def run_app():
        script_path = get_script_path(app)
        click.echo(f"[INFO] Script Path: {script_path}")
        app_instance = import_user_app(script_path)
        click.echo("[INFO] The application is running.")
        app_instance.run()

    if reload:
        script_path = get_script_path(app)
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


@click.group(help=f"theTrial CLI Tool v{__version__}")
@click.version_option(version=__version__, prog_name="theTrial")
def main():
    pass


main.add_command(init_command)
main.add_command(run_command)
