"""
File upload example for RVP.
"""
import sys
import os
import time
import requests

if len(sys.argv) != 3:
    print(
        "Please provide only the server address and a single filename. For example: ./client.py http://0.0.0.0:8080 file.zip")
    sys.exit(2)


def get_status(url: str) -> int:
    """
    Get result for a file hash of a uploaded file.
    """
    hash_response = requests.get(url, timeout=100)
    if hash_response.status_code == 102:
        time.sleep(2.4)
        return get_status(hash)
    else:
        return hash_response


URL = sys.argv[1]
FILENAME = sys.argv[2]

# Check if the file is available
if not os.path.isfile(FILENAME):
    print(f"The file {FILENAME} couldn't be found.")
    sys.exit(2)

# Testing the scanner
scanner_response = requests.get(f"{URL}/info", timeout=10)
if scanner_response.status_code != 200:
    print("The RVP scanner is not responding in a healthy manner.")
    sys.exit(2)

info = scanner_response.json()
scanner_name = info["scanner"]

print(f"[{scanner_name}]: Testing the file `{FILENAME}` for any threats")

with open(FILENAME, 'rb') as file:
    upload_response = requests.put(
        f"{URL}/{os.path.basename(FILENAME)}", data=file, timeout=None,)

file_hash = upload_response.text

resultcode = get_status(f"{URL}/resultof/{file_hash}")

if resultcode.status_code == 200:
    print(f"[{scanner_name}]: No threats found.")
    sys.exit(0)
elif resultcode.status_code == 406:
    threats_json = resultcode.json()
    threats_str = ", ".join(threats_json["threats"])
    print(f"[{scanner_name}]: Threats found! Threats: {threats_str}")
    sys.exit(1)
elif resultcode.status_code == 500:
    print(f"[{scanner_name}]: RVP has an error.")
    sys.exit(1)
