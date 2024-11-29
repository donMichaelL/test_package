import pytest

from theTrial import exceptions
from theTrial.utils.decorated_function_utils import validate_decorated_function


class TestValidateDecoratedFunction:
    def test_valid_function(self, dummy_data_class):
        """Validates that a properly annotated function with desirializer passes."""

        def valid_func(data: dummy_data_class):
            pass

        func, data_class = validate_decorated_function(valid_func)
        assert func == valid_func
        assert data_class == dummy_data_class

    def test_missing_annotation(self):
        """Checks that a function without type annotations raises an error."""

        def invalid_func(data):
            pass

        with pytest.raises(
            exceptions.MissingParameterAnnotationError, match="First parameter must have a type annotation"
        ):
            validate_decorated_function(invalid_func)

    def test_missing_desirializer_method(self, dummy_data_class_without_desirializer):
        """Ensures that a data class without desirializer raises an error."""

        def invalid_func(data: dummy_data_class_without_desirializer):
            pass

        with pytest.raises(exceptions.MissingDesirializerMethodError, match="must have a desirializer method"):
            validate_decorated_function(invalid_func)

    def test_function_with_no_arguments(self):
        """Confirms that functions with no arguments are handled correctly."""

        def no_arg_func():
            pass

        func, data_class = validate_decorated_function(no_arg_func)
        assert func == no_arg_func
        assert data_class is None
