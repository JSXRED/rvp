"""
Windows Defender
"""
import os
import re
import subprocess
from common.interface_scanner import IScanner
from common.response import Response
from common.enum_returncode import Returncodes


class WindowsDefender(IScanner):
    """
    Scanner as Windows Denfer
    """

    def __init__(self) -> None:
        self.logo = "Windows-defender.svg"
        self.name = "Windows Defender"

    def is_available(self) -> bool:
        """
        Check if Windows Defender is available.
        @returns bool: True if Windows Defender is available
        """
        program_files = os.environ.get("ProgramFiles", "")
        defender_path = os.path.join(
            program_files, "Windows Defender", "MpCmdRun.exe")
        return os.path.isfile(defender_path)

    def start_scan(self, filename: str) -> Response:
        """
        Scans the given file for any threats.
        """
        program_files = os.environ["ProgramFiles"]

        child = subprocess.Popen(
            f"{program_files}\\Windows Defender\\MpCmdRun.exe -Scan -ScanType 3 -DisableRemediation -File {filename}", stdout=subprocess.PIPE)

        streamdata = child.communicate()[0].decode(
            "utf-8").replace("\\r", "\r").replace("\\n", "\n")
        result = re.findall(r"Threat\s+:(.*)\r",
                            streamdata, flags=re.I | re.M | re.X)
        result = list(map(str.strip, result))

        rep = Response()
        rep.threats = result
        rep.log = streamdata

        if child.returncode == 0:
            rep.returncode = Returncodes.OK
        elif child.returncode == 2 and len(result) > 0:
            rep.returncode = Returncodes.INFECTED
        elif child.returncode == 2 and len(result) <= 0:
            rep.returncode = Returncodes.FISHY
        else:
            rep.returncode = Returncodes.FISHY

        return rep
