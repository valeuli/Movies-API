from enum import Enum

from app.utils.enum_utils import serialize_enums


class SampleTestEnum(Enum):
    OPTION_ONE = "Option 1"
    OPTION_TWO = "Option 2"


def test_serialize_enums_with_enums():
    """
    Test serialize_enums when dictionary contains Enum values.
    """
    input_data = {
        "key1": SampleTestEnum.OPTION_ONE,
        "key2": SampleTestEnum.OPTION_TWO,
        "key3": 42,
        "key4": "string_value",
    }

    expected_output = {
        "key1": "Option 1",
        "key2": "Option 2",
        "key3": 42,
        "key4": "string_value",
    }

    result = serialize_enums(input_data)
    assert result == expected_output


def test_serialize_enums_without_enums():
    """
    Test serialize_enums when dictionary does not contain Enum values.
    """
    input_data = {"key1": 42, "key2": "string_value", "key3": [1, 2, 3]}

    result = serialize_enums(input_data)
    assert result == input_data  # No cambios esperados


def test_serialize_enums_empty_dict():
    """
    Test serialize_enums with an empty dictionary.
    """
    input_data = {}

    result = serialize_enums(input_data)
    assert result == {}
