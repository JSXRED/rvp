"""
ESET Server Secruity
"""
import os
import re
import subprocess

from common.interface_scanner import IScanner
from common.response import Response
from common.enum_returncode import Returncodes


class Esset(IScanner):
    """
    Scanner as ESET Server Secruity
    """

    def __init__(self) -> None:
        self.logo = "csm_ESET_logo_DS_PP_horizontal_color_RGB_large_9199ef0732.png"
        self.name = "ESET Server Secruity"

    def is_available(self) -> bool:
        """
        Check if ESET Server Secruity is available.
        Returns:
            bool: True if ESET Server Secruity is available, False otherwise.
        """
        return os.path.isfile("/opt/eset/efs/sbin/cls/cls")

    def start_scan(self, filename: str) -> Response:
        """
        Scans the given file for threats using ESET Server Secruity.
        """
        cmd = "/opt/eset/efs/sbin/cls/cls --no-quarantine --log-console --log-all"
        child = subprocess.Popen(
            f"{cmd} {filename}", stdout=subprocess.PIPE, shell=True)
        streamdata = child.communicate()[0].decode(
            "utf-8").replace("\\r", "\r").replace("\\n", "\n")

        result = re.findall(r'result="(.*?)"',
                            streamdata, flags=re.I | re.M | re.X)
        result = list(map(str.strip, result))

        rep = Response()

        if child.returncode == 0:
            rep.returncode = Returncodes.OK
        elif child.returncode in (50, 1) and len(result) > 0:
            rep.returncode = Returncodes.INFECTED
        elif child.returncode in (100, 10):
            rep.returncode = Returncodes.FISHY
        else:
            rep.returncode = Returncodes.FISHY

        rep.threats = result
        rep.log = streamdata
        return rep
