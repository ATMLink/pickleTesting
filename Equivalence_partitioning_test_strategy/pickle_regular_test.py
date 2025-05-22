from test_input_regular import TEST_INPUTS
import pickle
import hashlib
import pytest
import sys
import os
from datetime import datetime

# Automatically generate a unique output file path
def get_output_file_path():
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    base_name = f"py_{version}"
    counter = 1

    while True:
        file_name = f"{base_name}_{counter:02d}.txt"
        file_path = os.path.join(os.getcwd(), file_name)
        if not os.path.exists(file_path):
            return file_path
        counter += 1

# Generate the output file path at module load
OUTPUT_FILE = get_output_file_path()

def setup_module(module):
    # Write initial information
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"Python version: {sys.version}\n")
        f.write(f"Test time: {datetime.now()}\n")
        f.write("=== Pickle Test Output ===\n\n")

def hash_pickle(obj):
    """Serialize object and return its SHA-256 hash"""
    return hashlib.sha256(pickle.dumps(obj, protocol=4)).hexdigest()

@pytest.mark.parametrize("data", TEST_INPUTS)
def test_regular_stability(data):
    """Test stability of regular data types: consistent hash after multiple serializations"""
    try:
        hash1 = hash_pickle(data)
        hash2 = hash_pickle(data)
        assert hash1 == hash2, f"Input {repr(data)} has inconsistent hash under protocol 4"
    except Exception as e:
        message = f"[Stability Skipped] Input: {repr(data)}\nReason: {type(e).__name__}: {e}\n\n"
        print(message)
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(message)


@pytest.mark.parametrize("data", TEST_INPUTS)
def test_regular_correctness(data):
    """Test correctness of regular data types: compare original and deserialized object hashes"""
    try:
        serialized = pickle.dumps(data, protocol=4)
        deserialized = pickle.loads(serialized)

        original_hash = hashlib.sha256(str(data).encode()).hexdigest()
        deserialized_hash = hashlib.sha256(str(deserialized).encode()).hexdigest()
        is_equal = original_hash == deserialized_hash

        output = (
            f"Input: {repr(data)}\n"
            f"Original object hash: {original_hash}\n"
            f"Deserialized object hash: {deserialized_hash}\n"
            f"Match: {is_equal}\n\n"
        )

        print(output)
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(output)
    except Exception as e:
        message = f"[Correctness Skipped] Input: {repr(data)}\nReason: {type(e).__name__}: {e}\n\n"
        print(message)
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(message)
