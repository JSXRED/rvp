"""
Enum of possible return codes
"""
from enum import Enum


class Returncodes(Enum):
    """
    States of possible returns
    """
    OK = 1
    """
    The file which is checked is fine
    """
    INFECTED = 2
    """
    The file is marked as infected
    """
    FISHY = -99
    """
    Something happend which interrupts the check. No valid repsonse is possible
    """
