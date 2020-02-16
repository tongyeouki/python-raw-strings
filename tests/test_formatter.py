import pytest

from raw_strings.formatter import DataFormatter
from tests.conftest import FakeType, FakeUser


class TestDataFormatter:
    def test_data_formatter_get_data_type(self):
        string = "Hello World"
        formatter = DataFormatter(data=string)
        assert formatter.instance.__class__.__name__ == "StringFormatter"

    def test_data_formatter_non_registered_type(self):
        data = FakeType
        escaped = DataFormatter(data=data).raw()
        assert escaped == data

    def test_add_custom_type(self):
        data = {"\bHello World\n", "\tBrand name", "John\6Doe"}
        formatted = DataFormatter(data=data).raw()
        assert formatted == {r"\bHello World\n", r"\tBrand name", r"John\6Doe"}

    def test_add_char_to_table(self):
        data = {'Hello zzz\n World\n', "\tBrand name", "John\6Doe"}
        formatter = DataFormatter(data=data)
        formatter.table.chars['zzz\n'] = r'zzz\n'
        assert formatter.table.add("zzz\n", r'zzz\n')
        expected = {r'\tBrand name', r'Hello zzz\n World\n', r'John\6Doe'}
        assert formatter.raw() == expected
        formatter.table.delete('zzz\n')

    def test_delete_char_from_table(self):
        data = {'\nHello World\n', "\nBrand name\n", "\nJohn Doe\n"}
        formatter = DataFormatter(data=data)
        formatter.table.delete("\n")
        with pytest.raises(KeyError):
            assert formatter.table.chars["\n"]
        expected = {'\nBrand name\n', '\nHello World\n', '\nJohn Doe\n'}
        assert formatter.raw() == expected
        formatter.table.add("\n", r"\n")


class TestStringFormatter:
    def test_raw_method(self):
        string = "\bHello World\n"
        formatted = DataFormatter(data=string).raw()
        assert formatted == r"\bHello World\n"

    def test_raw_method_with_upper(self):
        string = "\bHELLO WORLD\n"
        formatted = DataFormatter(data=string).raw()
        assert formatted == r"\bHELLO WORLD\n"


class TestDictFormatter:
    def test_raw_method(self):
        data = {"a": "\bHello World\n", "b": "\tBrand name", "c": "John\6Doe"}
        formatted = DataFormatter(data=data).raw()
        assert formatted == {"a": r"\bHello World\n", "b": r"\tBrand name", "c": r"John\6Doe"}

    def test_raw_method_with_integer_in_dict(self):
        data = {"a": "\bHello World\n", "b": "\tBrand name", "c": 1}
        formatted = DataFormatter(data=data).raw()
        assert formatted == {"a": r"\bHello World\n", "b": r"\tBrand name", "c": 1}

    def test_raw_method_with_float_in_dict(self):
        data = {"a": "\bHello World\n", "b": "\tBrand name", "c": 1.2345}
        formatted = DataFormatter(data=data).raw()
        assert formatted == {"a": r"\bHello World\n", "b": r"\tBrand name", "c": 1.2345}

    def test_raw_method_dict_contains_list(self):
        data = {"a": "\bHello World\n", "b": ["\bHello World\n", "\tBrand name", "John\6Doe"]}
        formatted = DataFormatter(data=data).raw()
        expected = {"a": r"\bHello World\n", "b": [r"\bHello World\n", r"\tBrand name", r"John\6Doe"]}
        assert formatted == expected


class TestListFormatter:
    def test_raw_method(self):
        data = ["\bHello World\n", "\tBrand name", "John\6Doe"]
        formatted = DataFormatter(data=data).raw()
        assert formatted == [r"\bHello World\n", r"\tBrand name", r"John\6Doe"]

    def test_raw_method_with_integer_in_list(self):
        data = ["\bHello World\n", "\tBrand name", 1]
        formatted = DataFormatter(data=data).raw()
        assert formatted == [r"\bHello World\n", r"\tBrand name", 1]

    def test_raw_method_with_float_in_list(self):
        data = ["\bHello World\n", "\tBrand name", 1.2345]
        formatted = DataFormatter(data=data).raw()
        assert formatted == [r"\bHello World\n", r"\tBrand name", 1.2345]

    def test_raw_list_contains_dict(self):
        data = ["\bHello World\n", {"a": "\bHello World\n", "b": "\tBrand name", "c": "John\6Doe"}]
        formatted = DataFormatter(data=data).raw()
        expected = [r"\bHello World\n", {"a": r"\bHello World\n", "b": r"\tBrand name", "c": r"John\6Doe"}]
        assert formatted == expected


class TestSetFormatter:
    def test_raw_method(self):
        data = {"\bHello World\n", "\tBrand name", "John\6Doe"}
        formatted = DataFormatter(data=data).raw()
        assert formatted == {r"\bHello World\n", r"\tBrand name", r"John\6Doe"}

    def test_raw_method_with_integer_in_set(self):
        data = {"\bHello World\n", "\tBrand name", 1}
        formatted = DataFormatter(data=data).raw()
        assert formatted == {r"\bHello World\n", r"\tBrand name", 1}

    def test_raw_method_with_float_in_set(self):
        data = {"\bHello World\n", "\tBrand name", 1.2345}
        formatted = DataFormatter(data=data).raw()
        assert formatted == {r"\bHello World\n", r"\tBrand name", 1.2345}


class TestTupleFormatter:
    def test_raw_method(self):
        data = ("\bHello World\n", "\tBrand name", "John\6Doe")
        formatted = DataFormatter(data=data).raw()
        assert formatted == (r"\bHello World\n", r"\tBrand name", r"John\6Doe")

    def test_raw_method_with_integer_in_list(self):
        data = ("\bHello World\n", "\tBrand name", 1)
        formatted = DataFormatter(data=data).raw()
        assert formatted == (r"\bHello World\n", r"\tBrand name", 1)

    def test_raw_method_with_float_in_tuple(self):
        data = ("\bHello World\n", "\tBrand name", 1.2345)
        formatted = DataFormatter(data=data).raw()
        assert formatted == (r"\bHello World\n", r"\tBrand name", 1.2345)


class TestWithNestedData:
    def test_raw_method_with_object(self):
        user = FakeUser()
        formatted = DataFormatter(data=user).raw()
        assert formatted == user
        assert formatted is user
        assert formatted.first_name == r"\bJohn\b"
        assert formatted.last_name == r"\bDoe\b"
        assert formatted.password == r"pass\l?word\r"
