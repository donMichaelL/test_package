import importlib.util
import os
import sys

from ..app import TheTrial
from ..exceptions import AppImportError
from ..exceptions import ScriptPathError


def create_file(path: str, filename: str, content: str = "") -> None:
    """Create a file with the specified content at the given path and filename."""
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, filename), "w") as file:
        file.write(content)


def check_script_existence(script_path):
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

    app = user_module.app
    if not isinstance(app, TheTrial):
        raise AppImportError(f"The 'app' object in '{user_module.__name__}.py' " "is not an instance of TheTrial.")

    return app


def import_user_app(script_path):
    """Dynamically import the user-defined module and return the 'app' object if it exists."""
    script_dir = os.path.dirname(script_path)
    sys.path.insert(0, script_dir)

    spec = get_module_spec(script_path)
    user_module = load_module_from_spec(spec)
    return get_app_instance(user_module)
