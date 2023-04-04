"""
RVP server provides all needed endpoints
"""
import os
import shutil
import time
import threading
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from dotenv import load_dotenv
from jinja2 import Template
from common.rvp import RVP
from common.enum_returncode import Returncodes

load_dotenv()


class RVPserver(BaseHTTPRequestHandler):
    """
    Basic HTTP - Server to handle file transfers and status of scans
    """

    __rvp = RVP()

    def do_PUT(self):
        """
        Handle file upload over PUT Method
        """
        filename = os.path.basename(self.path)
        if not filename:
            filename = "unkown"
        request_time = int(time.time())
        filepath = f"{self.__rvp.storage_vault}/{request_time}___{filename}"

        file_length = int(self.headers['Content-Length'])
        with open(filepath, 'wb') as output_file:
            output_file.write(self.rfile.read(file_length))

        # File hash the uploaded file
        filehash = self.__rvp.get_md5filehash(filepath)
        with open(f"{self.__rvp.storage_db}/{filehash}", mode='w', encoding="utf8"):
            pass

        # Start scanning of the uploaded file
        scan_thread = threading.Thread(target=self.__rvp.scan_file,
                                       name="ScanProcessor", args=(filepath, filehash,))
        try:
            scan_thread.start()
        except IOError:
            pass
        finally:
            # Ensure that the thread is properly cleaned up
            scan_thread.join()

        # Write output
        self.protocol_version = 'HTTP/1.0'
        self.send_response(200, 'OK')
        self.end_headers()
        self.wfile.write(filehash.encode('utf-8'))

    def do_GET(self):
        """
        Handle GET requests
        """
        path = self.path.replace("//", "/")
        if path.startswith("/info"):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            info = {"status": "OK", "scanner": self.__rvp.scanner.name}
            self.wfile.write(
                bytes(json.dumps(info), "utf-8"))
            return

        if path.startswith("/resultof/"):
            filehash = path.replace("/resultof/", "")
            if os.path.exists(f"{self.__rvp.storage_db}/{filehash}"):
                with open(f"{self.__rvp.storage_db}/{filehash}", mode="r", encoding="utf8") as file:
                    content = file.read()
                    if not content:
                        self.send_response_only(102)
                        return

                    filestatus = json.loads(content)
                    if filestatus["returncode"] == Returncodes.OK.name:
                        self.send_response(200)

                    elif filestatus["returncode"] == Returncodes.INFECTED.name:
                        self.send_response(406)
                    else:
                        self.send_response(500)

                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(
                        bytes(content, "utf-8"))
                    return
            else:
                self.send_response_only(404)
                return

        path = f"www{path}"
        if path == "www/":
            path = "www/index.html"

        if os.path.exists(path):
            self.send_response(200)
            contenttype = "text/html"

            if ".svg" in path:
                contenttype = "image/svg+xml"
            elif ".png" in path:
                contenttype = "image/png"

            self.send_header("Content-type", contenttype)
            self.end_headers()
            with open(path, "rb") as content:
                if path == "www/index.html":
                    response = content.read().decode("utf-8")
                    response = Template(response)
                    response = response.render(obj=self.__rvp)
                    self.wfile.write(
                        bytes(response, "utf-8"))
                else:
                    shutil.copyfileobj(content, self.wfile)
        else:
            self.send_response_only(404)

        self.send_response_only(500)
        return

    def log_message(self, format, *args):
        """
        Make the HTTP-Server silence
        """
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == "__main__":
    port = os.getenv("HTTP_PORT")
    webServer = ThreadedHTTPServer(
        ("0.0.0.0", int(port)), RVPserver)
    print(f"RVP Server started http://0.0.0.0:{port}, use <Ctrl-C> to stop")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("RVP Server stopped.")
