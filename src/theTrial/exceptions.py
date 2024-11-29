class ScriptPathError(Exception):
    """Exception for errors related to obtaining the script path."""


class AppImportError(Exception):
    """
    Custom exception for errors related to importing the
    user-defined application.
    """


class MissingSerializeMethodError(Exception):
    def __init__(self, obj):
        message = (
            f"The object of type '{type(obj).__name__}' does not "
            "have a 'serializer' method. Please define a 'serialize' method "
            "in your class."
        )
        super().__init__(message)


class FunctionValidationError(Exception):
    """Base exception for function validation errors."""


class MissingParameterAnnotationError(FunctionValidationError):
    """Raised when the first parameter lacks a type annotation."""


class MissingDesirializerMethodError(FunctionValidationError):
    """Raised when the annotated data class lacks a desirializer method."""
