"""
CalmAV
"""
import shutil
import re
import subprocess

from common.interface_scanner import IScanner
from common.response import Response
from common.enum_returncode import Returncodes


class ClamAV(IScanner):
    """
    Scanner as ClamAV
    """

    def __init__(self) -> None:
        self.logo = "clamav_logo.png"
        self.name = "ClamAV"

    def is_available(self) -> bool:
        """
        Check if ClamAV is available.
        Returns:
            bool: True if ClamAV is available, False otherwise.
        """
        return shutil.which("clamscan") is not None

    def start_scan(self, filename: str) -> Response:
        """
        Scans the given file for threats using ClamAV.
        """
        cmd = shutil.which("clamscan")
        child = subprocess.Popen(
            f"{cmd} {filename}", stdout=subprocess.PIPE, shell=True)
        streamdata = child.communicate()[0].decode(
            "utf-8").replace("\\r", "\r").replace("\\n", "\n")
        result = re.findall(r": (.*) FOUND",
                            streamdata, flags=re.I | re.M | re.X)
        result = list(map(str.strip, result))

        rep = Response()

        if child.returncode == 0:
            rep.returncode = Returncodes.OK
        elif child.returncode == 1 and len(result) > 0:
            rep.returncode = Returncodes.INFECTED
        elif child.returncode == 2:
            rep.returncode = Returncodes.FISHY
        else:
            rep.returncode = Returncodes.FISHY

        rep.threats = result
        rep.log = streamdata
        return rep
