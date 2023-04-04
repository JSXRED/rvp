"""
Interface for Scanner
"""


class Response:
    """
    Response Class
    """
    def __init__(self) -> None:
        pass

    filehash: str = None
    """
    checksum of the file
    """
    threats: list = ()
    """
    String list of threats
    """
    returncode: int = -1
    """
    0=No threats found, 1= Threats found, -99 = Something is fishy
    """
    log: str = None
    """
    Plain log of scanner
    """
