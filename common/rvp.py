"""
This file include the class of RVP
"""
import os
import platform
import hashlib
import json
from common.scanner import windowsdefender as wd
from common.scanner import clamav as cl
from common.scanner import eset as es
from common import interface_scanner
from common import response


class RVP:
    """
    RVP Class
    """
    scanner: interface_scanner = None
    storage_path = f"{os.path.dirname(__file__)}/../storage"
    storage_db = f"{storage_path}/db"
    storage_vault = f"{storage_path}/__vault"

    def __init__(self) -> None:
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(self.storage_db, exist_ok=True)
        os.makedirs(self.storage_vault, exist_ok=True)

        self.scanner = self.__get_scanner()

    def __get_scanner(self) -> interface_scanner:
        systemname = platform.system()
        if systemname == "Windows":
            # Test if Windows Defender is available
            wd_scanner = wd.WindowsDefender()
            if wd_scanner.is_available():
                return wd_scanner
        elif systemname == "Linux":
            # Test if ClamAV is available
            cl_scanner = cl.ClamAV()
            if cl_scanner.is_available():
                return cl_scanner
            # Test if esset is available
            es_scanner = es.Esset()
            if es_scanner.is_available():
                return es_scanner
            return ""
        else:
            raise OSError("Unknown system or no scanner found")
        return None

    def scan_file(self, file: str, filehash: str) -> response.Response:
        """
        Scan file
        """
        rep = self.scanner.start_scan(file)
        rep.filehash = filehash

        with open(f"{self.storage_db}/{filehash}", mode="w", encoding="utf-8") as dbfile:
            dbfile.write(json.dumps(rep.__dict__, default=lambda x: x.name))

        os.unlink(file)
        return rep

    def get_md5filehash(self, file):
        """
        Generate a filehash based on the uploaded file
        """
        hash_md5 = hashlib.md5()
        with open(file, "rb") as filechunk:
            for chunk in iter(lambda: filechunk.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
