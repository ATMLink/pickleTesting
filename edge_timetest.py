import pickle
import timeit
import unittest
import sys
import subprocess
import tempfile

PYTHON_VERSIONS = ["3.7", "3.8", "3.9"]
PICKLE_PROTOCOL = 4

def run_pickle_test(python_version, data, protocol=PICKLE_PROTOCOL):
    """在指定的 Python 版本中运行 pickle 序列化和反序列化，并返回结果."""
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            temp_file_name = tmpfile.name

        script = f"""
import pickle
import hashlib

data = {data!r}
protocol = {protocol}

try:
    pickled_data = pickle.dumps(data, protocol=protocol)
    unpickled_data = pickle.loads(pickled_data)
    hash_value = hashlib.sha256(pickle.dumps(unpickled_data, protocol=protocol)).hexdigest()
    print(hash_value)
except Exception as e:
    print(f"ERROR: {{e}}")
"""
        result = subprocess.run(
            [sys.executable.replace(sys.version[:3], python_version), "-c", script],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print(f"Python {python_version} 错误输出:\n{result.stderr}")
            return None

        return result.stdout.strip()

    except subprocess.TimeoutExpired:
        print(f"Python {python_version} 运行超时")
        return None
    except FileNotFoundError:
        print(f"未找到 Python {python_version} 可执行文件")
        return None


class PickleSpecificTest(unittest.TestCase):

    def test_large_string_performance(self):
        """测试大型字符串的性能."""
        large_string = "a" * 2**20  # 1MB 字符串
        print("\nTesting large string performance:")
        times = {}
        for version in PYTHON_VERSIONS:
            try:
                # 使用 timeit 测量序列化和反序列化的时间
                setup = f"import pickle; data = {large_string!r}; protocol = {PICKLE_PROTOCOL}"
                stmt = "pickle.dumps(data, protocol=protocol); pickle.loads(pickle.dumps(data, protocol=protocol))"
                time = timeit.timeit(stmt, setup=setup, number=10)  # 运行 10 次
                times[version] = time
                print(f"Python {version}: {time:.4f} seconds")
            except Exception as e:
                print(f"Python {version} 运行失败: {e}")
        #比较性能，这里可以设置断言，例如3.9版本应该比3.7快
        if "3.9" in times and "3.7" in times:
            self.assertLess(times["3.9"], times["3.7"], "Python 3.9 should be faster than Python 3.7")

if __name__ == "__main__":
    unittest.main()
