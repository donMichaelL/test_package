from collections.abc import Callable
from inspect import signature
from typing import Any
from typing import Tuple

from ..exceptions import MissingDesirializerMethodError
from ..exceptions import MissingParameterAnnotationError


def validate_decorated_function(func: Callable) -> Tuple[Callable, Any]:
    """
    Validate the function passed to the intopic decorator.

    Raises:
        MissingParameterAnnotationError: If the first parameter lacks a type annotation.
        MissingFromJsonMethodError: If the annotated data class lacks a desirializer method.
    """
    sig = signature(func)
    params = list(sig.parameters.values())
    if not params:
        return func, None

    first_param = params[0]
    data_class = first_param.annotation
    if data_class is first_param.empty:
        raise MissingParameterAnnotationError("First parameter must have a type annotation")

    if not hasattr(data_class, "desirializer") or not callable(getattr(data_class, "desirializer", None)):
        raise MissingDesirializerMethodError(f"The annotation '{data_class.__name__}' must have a desirializer method")

    return func, data_class
