import pickle
import hashlib
import random
import sys
import unittest
import subprocess
import tempfile
import os
import platform

# 测试用的 Python 版本列表
PYTHON_VERSIONS = ["3.7", "3.8", "3.9"]
PICKLE_PROTOCOL = 4  # 统一使用 pickle 协议 4

def calculate_hash(data):
    """计算数据的 SHA-256 哈希值."""
    return hashlib.sha256(data).hexdigest()

def run_pickle_test(python_version, data):
    """在指定的 Python 版本中运行 pickle 序列化和反序列化，并返回哈希值."""
    try:
        # 创建一个临时文件来存储 pickle 数据
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            temp_file_name = tmpfile.name

        # 使用 subprocess 调用指定的 Python 版本来执行序列化和反序列化
        script = f"""
import pickle
import hashlib

data = {data!r}  # 使用 repr() 确保数据被正确传递
protocol = {PICKLE_PROTOCOL}

try:
    # 序列化
    pickled_data = pickle.dumps(data, protocol=protocol)

    # 反序列化
    unpickled_data = pickle.loads(pickled_data)

    # 计算反序列化数据的哈希值
    hash_value = hashlib.sha256(pickle.dumps(unpickled_data, protocol=protocol)).hexdigest()

    print(hash_value)
except Exception as e:
    print(f"ERROR: {{e}}")
"""
        result = subprocess.run(
            [sys.executable.replace(sys.version[:3], python_version), "-c", script],
            capture_output=True,
            text=True,
            timeout=10  # 设置超时时间
        )

        if result.returncode != 0:
            print(f"Python {python_version} 错误输出:\n{result.stderr}")
            return None  # 返回 None 表示出错

        return result.stdout.strip()  # 返回哈希值

    except subprocess.TimeoutExpired:
        print(f"Python {python_version} 运行超时")
        return None
    except FileNotFoundError:
        print(f"未找到 Python {python_version} 可执行文件")
        return None

class PickleCompatibilityTest(unittest.TestCase):
    """测试 pickle 兼容性的 unittest 类."""

    def test_boundary_data(self):
        """测试边界数据和超边界数据的序列化和反序列化，并进行统计分析."""

        # 整数边界
        int_min = -(2**63)
        int_max = 2**63 - 1

        # 字符串边界
        empty_string = ""
        short_string = "a"
        long_string = "a" * (2**10)  # 1KB
        very_long_string = "a" * (2**16) # 64KB

        # 列表边界
        empty_list = []
        short_list = [1]
        long_list = list(range(2**8)) # 256
        very_long_list = list(range(2**10)) # 1024

        # 字典边界
        empty_dict = {}
        short_dict = {1: "a"}
        long_dict = {i: str(i) for i in range(2**8)} # 256
        very_long_dict = {i: str(i) for i in range(2**10)} # 1024

        # 元组边界
        empty_tuple = ()
        short_tuple = (1,)
        long_tuple = tuple(range(2**8)) # 256
        very_long_tuple = tuple(range(2**10)) # 1024

        # 浮点数边界
        float_min = -1e300
        float_max = 1e300
        float_zero = 0.0
        float_one = 1.0
        float_neg_one = -1.0
        float_nan = float('nan')
        float_inf = float('inf')
        float_neg_inf = float('-inf')

        test_data = [
            # 整数边界
            0,
            1,
            -1,
            int_min,
            int_max,
            int_min + 1,
            int_max - 1,
            int_min - 1, #超出范围
            int_max + 1,  #超出范围

            # 字符串边界
            empty_string,
            short_string,
            long_string,
            very_long_string,

            # 列表边界
            empty_list,
            short_list,
            long_list,
            very_long_list,

            # 字典边界
            empty_dict,
            short_dict,
            long_dict,
            very_long_dict,

            # 元组边界
            empty_tuple,
            short_tuple,
            long_tuple,
            very_long_tuple,

             # 浮点数边界
            float_min,
            float_max,
            float_zero,
            float_one,
            float_neg_one,
            float_nan,
            float_inf,
            float_neg_inf,
            1e-300, # 接近0的浮点数
            -1e-300,

            # 集合边界
            set(),
            {1},
            frozenset(),
            frozenset({1}),
        ]

        results = {}  # 存储每个测试数据的哈希值和状态
        version_stats = {version: {"success": 0, "failure": 0, "error": 0} for version in PYTHON_VERSIONS} # 存储每个版本的统计信息

        for data in test_data:
            data_str = repr(data)  # 获取数据的字符串表示形式
            print(f"\n测试数据: {data_str}")
            results[data_str] = {}  # 初始化该数据的字典

            hashes = {}
            for version in PYTHON_VERSIONS:
                hash_value = run_pickle_test(version, data)
                if hash_value:
                    hashes[version] = hash_value
                    results[data_str][version] = "success"  # 记录成功
                    version_stats[version]["success"] += 1
                    print(f"Python {version} 哈希值: {hash_value}")
                else:
                    results[data_str][version] = "failure"  # 记录失败
                    version_stats[version]["failure"] += 1
                    print(f"Python {version} 运行失败，跳过比较")

            # 比较不同版本之间的哈希值
            if len(hashes) > 1:
                first_version = PYTHON_VERSIONS[0]
                if first_version in hashes:
                    first_hash = hashes[first_version]
                    for version, hash_value in hashes.items():
                        try:
                            self.assertEqual(
                                first_hash,
                                hash_value,
                                f"Python {first_version} 和 Python {version} 的哈希值不匹配!"
                            )
                        except AssertionError as e:
                            print(e)
                            version_stats[version]["error"] += 1 # 记录错误
                            results[data_str][version] = "error"
                else:
                    print(f"跳过哈希值比较，因为 Python {first_version} 运行失败")
            else:
                print("只有一个 Python 版本成功运行，无法进行比较")

        # 打印统计信息
        print("\n--- 统计信息 ---")
        for version, stats in version_stats.items():
            print(f"Python {version}:")
            print(f"  成功: {stats['success']}")
            print(f"  失败: {stats['failure']}")
            print(f"  错误: {stats['error']}")

        # 打印每个测试数据的详细结果
        print("\n--- 详细结果 ---")
        for data_str, version_results in results.items():
            print(f"数据: {data_str}")
            for version, result in version_results.items():
                print(f"  Python {version}: {result}")

if __name__ == "__main__":
    unittest.main()
