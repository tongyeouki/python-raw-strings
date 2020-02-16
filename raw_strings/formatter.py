import datetime
from copy import deepcopy

from raw_strings.base_formatter import BaseFormatter
from raw_strings.table import Table


class Formatter(BaseFormatter):
    types = {}

    def __init__(self, data):
        self.table = Table()
        self.data = data
        self.register()

    @classmethod
    def register(cls):
        """Register data types for mapping"""
        cls.types[dict] = DictFormatter
        cls.types[int] = EscapedData
        cls.types[float] = EscapedData
        cls.types[list] = ListFormatter
        cls.types[set] = SetFormatter
        cls.types[str] = StringFormatter
        cls.types[tuple] = TupleFormatter
        cls.types[type(None)] = EscapedData
        cls.types[type] = EscapedData
        cls.types[datetime.datetime] = EscapedData
        return cls

    def raw(self):
        """"""


class DataFormatter(Formatter):
    @property
    def instance(self):
        data_type = type(self.data)
        formatter = self.types.get(data_type)
        if not formatter:
            try:
                return ObjectFormatter(data=self.data)
            except Exception:
                return EscapedData(data=self.data)
        return formatter(self.data)

    def raw(self):
        return self.instance.raw()


class EscapedData:
    """Fake data structure which returns the native object"""
    def __init__(self, data):
        self.data = data

    def raw(self):
        return self.data


class StringFormatter(Formatter):
    def _raw(self, data):
        result = ''
        try:
            for char in data:
                try:
                    result += self.table.chars[char]
                except KeyError:
                    result += char
            return result
        except Exception:
            return data

    def raw(self):
        return self._raw(self.data)


class DictFormatter(StringFormatter):
    def raw(self):
        data = deepcopy(self.data)
        for key, value in data.items():
            self.data[key] = DataFormatter(data=value).raw()
        return self.data


class ObjectFormatter(StringFormatter):
    def raw(self):
        try:
            data = self.data.__dict__
            formatter = DataFormatter(data=data).raw()
            self.rebuild_instance(**formatter)
            return self.data
        except Exception:
            return EscapedData(data=self.data)

    def rebuild_instance(self, **kwargs):
        try:
            for attribute, value in kwargs.items():
                setattr(self.data, attribute, value)
        except Exception:
            return EscapedData(data=self.data)


class ListFormatter(StringFormatter):
    def raw(self):
        return [DataFormatter(data=value).raw() for value in self.data]


class SetFormatter(StringFormatter):
    def raw(self):
        data = set()
        for value in self.data:
            data.add(DataFormatter(data=value).raw())
        return data


class TupleFormatter(StringFormatter):
    def raw(self):
        return tuple([DataFormatter(data=value).raw() for value in self.data])
