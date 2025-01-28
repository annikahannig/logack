
import subprocess

def qrencode(data, fmt="svg"):
    """
    Encode data as qr code.
    """
    if not data:
        return None

    data = bytes(data, "UTF-8")
    fmt = fmt.upper()

    command = ["qrencode", "-o", "-", "-t", fmt]
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    stdout, _stderr = process.communicate(data)
    return stdout

