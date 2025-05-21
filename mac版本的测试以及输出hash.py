import os
import pickle
import hashlib
import uuid
import socket
import struct
import threading
from pathlib import Path

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def show_pickle_hash(name, obj):
    try:
        data = pickle.dumps(obj, protocol=4)
        print(f"{name:35} SHA256 = {sha256_hex(data)}")
    except Exception as e:
        print(f"{name:35} FAILED: {e}")

print("=== Pickle Hashes (Protocol 4) ===")
print(f"Platform: {os.name}, System: {os.uname().sysname}, Version: {os.uname().version}\n")

# Case 1: os.stat() result
show_pickle_hash("Case 1: os.stat('.')", os.stat("."))

# Case 2: socket object
sock = socket.socket()
show_pickle_hash("Case 2: socket.socket()", sock)
sock.close()

# Case 3: MAC address
class DeviceInfo:
    def __init__(self):
        self.mac = uuid.getnode()
show_pickle_hash("Case 3: uuid.getnode()", DeviceInfo())

# Case 4: Path object
show_pickle_hash("Case 4: Path('C:/Windows')", Path("C:/Windows/System32"))

# Case 5: struct.Struct
show_pickle_hash("Case 5: struct.Struct('i')", struct.Struct("i"))

# Case 6: frozenset as dict key
class CustomObject:
    def __init__(self):
        self.data = {
            frozenset(['x', 'y']): (1, 2),
            frozenset(['a', 'b']): (3, 4)
        }
# Fix hash seed to ensure stability on this OS


# os.environ['PYTHONHASHSEED'] = '42'
# show_pickle_hash("Case 6: frozenset dict key", CustomObject())
# === Pickle Hashes (Protocol 4) ===
# Platform: posix, System: Darwin, Version: Darwin Kernel Version 22.6.0: Tue Nov  7 21:42:31 PST 2023; root:xnu-8796.141.3.702.9~2/RELEASE_ARM64_T8112
#
# Case 1: os.stat('.')                SHA256 = 5546cad9c0636eabb2f423b2c0fe0400757856750d7081c5b9883fbde461b547
# Case 2: socket.socket()             FAILED: cannot pickle 'socket' object
# Case 3: uuid.getnode()              SHA256 = b7d6f850a17d92ef33be3c764caa0b1222db83f81150d0bd0f881b2fdc18e46b
# Case 4: Path('C:/Windows')          SHA256 = d03a985f39743a9651582c81df8d703d3a7a6f18b714e8d748774ccdb0e69894
# Case 5: struct.Struct('i')          FAILED: cannot pickle '_struct.Struct' object
# Case 6: frozenset dict key          SHA256 = 97f86e0446e235c5789db7b8711034b0305e157de8467f47c5839bb7cf9ad6f7
#
# Process finished with exit code 0