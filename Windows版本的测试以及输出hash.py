import os
import platform
import pickle
import hashlib
import uuid
import socket
import struct
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
print(f"Platform: {os.name}, System: {platform.system()}, Version: {platform.version()}\n")

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

# os.environ['PYTHONHASHSEED'] = '42'
show_pickle_hash("Case 6: frozenset dict key", CustomObject())

# Platform: nt, System: Windows, Version: 10.0.19045
# Case 1: os.stat('.')                SHA256 = 17f7367c99e7e432d13dc689357f8cb8bc6bad9148280fa966375187c1374b1a
# Case 2: socket.socket()             FAILED: cannot pickle 'socket' object
# Case 3: uuid.getnode()              SHA256 = 0c8d17a53aee3e77c98b1922881f56e8bd5fa85ae20aa31bc0dd2304cf80c0da
# Case 4: Path('C:/Windows')          SHA256 = a73e60d0c1e5981542d05b660ab4051a34f2a8d055321e7b610afa4f6b445747
# Case 5: struct.Struct('i')          FAILED: cannot pickle '_struct.Struct' object
# Case 6: frozenset dict key          SHA256 = 97f86e0446e235c5789db7b8711034b0305e157de8467f47c5839bb7cf9ad6f7