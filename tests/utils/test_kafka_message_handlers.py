from theTrial.utils import call_handlers


class TestCallHandlers:
    def test_no_argument_function(self, mock_message, mock_function):
        """Ensure functions with no arguments are called correctly."""
        no_arg_func = mock_function(arg_count=0)

        func_map = {"example-topic": [(no_arg_func, None)]}
        call_handlers(func_map, mock_message)
        no_arg_func.assert_called_once_with()

    def test_single_argument_function(self, mock_message, mock_function, dummy_data_class):
        """Ensure functions with a single argument are called correctly."""
        single_arg_func = mock_function(arg_names=("instance",), arg_count=1)

        func_map = {"example-topic": [(single_arg_func, dummy_data_class)]}
        call_handlers(func_map, mock_message)
        single_arg_func.assert_called_once_with({"deserialized_data": {"key": "value"}})

    def test_multi_argument_function(self, mock_message, mock_function, dummy_data_class):
        """Ensure functions with multiple arguments are called correctly."""
        multi_arg_func = mock_function(
            arg_names=("instance", "topic", "partition", "offset", "key", "timestamp"),
            arg_count=6,
        )

        func_map = {"example-topic": [(multi_arg_func, dummy_data_class)]}
        call_handlers(func_map, mock_message)
        multi_arg_func.assert_called_once_with(
            {"deserialized_data": {"key": "value"}},
            topic="example-topic",
            partition=0,
            offset=123,
            key="key",
            timestamp=(1, 16777216),
        )
