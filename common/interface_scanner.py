"""
BaseTemplate for virus scanner
"""
from abc import ABC, abstractmethod
from common.response import Response


class IScanner(ABC):
    """
    Interface for a virus scanner.
    """

    _logo = None
    """
    Path of the logo
    """
    _name = None
    """
    Name of the scanner
    """

    @abstractmethod
    def start_scan(self, filename: str) -> Response:
        """
        Scans the given file for viruses and returns a response object.
        :param filename: the path of the file to scan.
        :return: a Response object indicating whether the file is infected or not.
        """

    @abstractmethod
    def is_available(self) -> bool:
        """
        Checks whether the scanner is available on the system.
        :return: True if the scanner is available, False otherwise.
        """

    @property
    def name(self):
        """
        Get name of the scanner
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Set name of the scanner
        """
        self._name = value

    @property
    def logo(self):
        """
        Get logo of the scanner
        """
        return self._logo

    @logo.setter
    def logo(self, value):
        """
        Set logo of the scanner
        """
        self._logo = value
