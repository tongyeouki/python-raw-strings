from abc import ABC, abstractmethod


class BaseFormatter(ABC):
    """Defines base class for formatter"""

    @abstractmethod
    def raw(self):
        """"""
