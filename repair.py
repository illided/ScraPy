from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod


class HTMLRepair(metaclass=ABCMeta):
    @property
    @abstractmethod
    def original(self):
        ...

    @property
    @abstractmethod
    def repaired(self):
        ...


class BeautifulSoupRepair(HTMLRepair):
    def __init__(self, document):
        self._original = document
        soup = BeautifulSoup(document, 'html.parser')
        self._repaired = soup.prettify()

    def original(self):
        return self._original

    def repaired(self):
        return self._repaired
