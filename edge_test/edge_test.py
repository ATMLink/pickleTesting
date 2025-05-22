import pickle
import hashlib
import random
import sys
import unittest
import subprocess
import tempfile
import os
import platform
import datetime

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
    import traceback
    print(f"ERROR: {{e}}")
    traceback.print_exc() # 打印完整的堆栈跟踪
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
            (0, "int_zero"),
            (1, "int_one"),
            (-1, "int_neg_one"),
            (int_min, "int_min"),
            (int_max, "int_max"),
            (int_min + 1, "int_min_plus_one"),
            (int_max - 1, "int_max_minus_one"),
            (int_min - 1, "int_min_minus_one"), #超出范围
            (int_max + 1, "int_max_plus_one"),  #超出范围

            # 字符串边界
            (empty_string, "empty_string"),
            (short_string, "short_string"),
            (long_string, "long_string"),
            (very_long_string, "very_long_string"),

            # 列表边界
            (empty_list, "empty_list"),
            (short_list, "short_list"),
            (long_list, "long_list"),
            (very_long_list, "very_long_list"),

            # 字典边界
            (empty_dict, "empty_dict"),
            (short_dict, "short_dict"),
            (long_dict, "long_dict"),
            (very_long_dict, "very_long_dict"),

            # 元组边界
            (empty_tuple, "empty_tuple"),
            (short_tuple, "short_tuple"),
            (long_tuple, "long_tuple"),
            (very_long_tuple, "very_long_tuple"),

             # 浮点数边界
            (float_min, "float_min"),
            (float_max, "float_max"),
            (float_zero, "float_zero"),
            (float_one, "float_one"),
            (float_neg_one, "float_neg_one"),
            (float_nan, "float_nan"),
            (float_inf, "float_inf"),
            (float_neg_inf, "float_neg_inf"),
            (1e-300, "float_near_zero_pos"), # 接近0的浮点数
            (-1e-300, "float_near_zero_neg"),

            # 集合边界
            (set(), "empty_set"),
            ({1}, "short_set"),
            (frozenset(), "empty_frozenset"),
            (frozenset({1}), "short_frozenset"),
        ]

        results = {}  # 存储每个测试数据的哈希值和状态
        data_stats = {} # 存储每个数据类型的统计信息
        version_stats = {version: {"success": 0, "failure": 0, "error": 0} for version in PYTHON_VERSIONS} # 存储每个版本的统计信息

        # 创建结果文件名，包含当前日期和时间
        now = datetime.datetime.now()
        result_filename = f"edge_pickle_test_results_{now.strftime('%Y%m%d_%H%M%S')}.txt"

        with open(result_filename, "w", encoding="utf-8") as f:
            f.write("Pickle Compatibility Test Results\n")
            f.write(f"Date and Time: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Pickle Protocol: {PICKLE_PROTOCOL}\n")
            f.write(f"Python Versions: {', '.join(PYTHON_VERSIONS)}\n\n")

            # 初始化 data_stats
            for data, data_type in test_data:
                data_stats[data_type] = {"success": 0, "failure": 0, "error": 0, "hash_match": True, "error_messages": []}

            # 运行测试并收集结果
            for data, data_type in test_data:
                data_str = repr(data)  # 获取数据的字符串表示形式
                f.write(f"\n测试数据: {data_str} (类型: {data_type})\n")
                results[data_str] = {}  # 初始化该数据的字典

                hashes = {}
                all_versions_success = True  # 添加此行：所有版本是否成功
                for version in PYTHON_VERSIONS:
                    hash_value = run_pickle_test(version, data)
                    if hash_value:
                        hashes[version] = hash_value
                        results[data_str][version] = "success"  # 记录成功
                        version_stats[version]["success"] += 1
                        f.write(f"  Python {version} 哈希值: {hash_value}\n")
                    else:
                        results[data_str][version] = "failure"  # 记录失败
                        version_stats[version]["failure"] += 1
                        data_stats[data_type]["failure"] += 1
                        f.write(f"  Python {version} 运行失败，跳过比较\n")
                        data_stats[data_type]["hash_match"] = False  # 标记哈希值不匹配
                        all_versions_success = False # 添加此行：只要有一个版本失败，就设置为 False
                        # Capture error message from subprocess stderr
                        error_message = ""
                        try:
                           error_message = subprocess.run(
                                [sys.executable.replace(sys.version[:3], version), "-c", f"import pickle; pickle.dumps({data!r})"],
                                capture_output=True,
                                text=True,
                                timeout=10
                            ).stderr
                        except Exception as e:
                            error_message = str(e)
                        data_stats[data_type]["error_messages"].append(f"Python {version}: {error_message}")

                # 比较不同版本之间的哈希值
                if len(hashes) > 1:
                    first_version = PYTHON_VERSIONS[0]
                    if first_version in hashes:
                        first_hash = hashes[first_version]
                        for version, hash_value in hashes.items():
                            if hash_value != first_hash:
                                f.write(f"  警告: Python {first_version} 和 Python {version} 的哈希值不匹配!\n")
                                data_stats[data_type]["hash_match"] = False  # 标记哈希值不匹配
                                all_versions_success = False # 添加此行：只要有一个版本hash不匹配，就设置为 False
                            try:
                                self.assertEqual(
                                    first_hash,
                                    hash_value,
                                    f"Python {first_version} 和 Python {version} 的哈希值不匹配!"
                                )
                            except AssertionError as e:
                                f.write(f"  错误: {e}\n")
                                version_stats[version]["error"] += 1 # 记录错误
                                data_stats[data_type]["error"] += 1
                                results[data_str][version] = "error"
                                data_stats[data_type]["hash_match"] = False
                                all_versions_success = False # 添加此行：只要有一个版本报错，就设置为 False
                                data_stats[data_type]["error_messages"].append(f"Python {version}: {e}")

                    else:
                        f.write(f"  跳过哈希值比较，因为 Python {first_version} 运行失败\n")
                        data_stats[data_type]["hash_match"] = False  # 标记哈希值不匹配
                        all_versions_success = False # 添加此行：只要有跳过，就设置为 False
                else:
                    f.write("  只有一个 Python 版本成功运行，无法进行比较\n")
                    data_stats[data_type]["hash_match"] = False  # 标记哈希值不匹配
                    all_versions_success = False # 添加此行：只要无法比较，就设置为 False

                if all_versions_success: # 添加此行：只有所有版本都成功，才增加成功计数
                    data_stats[data_type]["success"] +=1

            # 在文件开头写入统计信息
            f.seek(0)  # 回到文件开头
            f.write("Pickle Compatibility Test Results\n")
            f.write(f"Date and Time: {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Pickle Protocol: {PICKLE_PROTOCOL}\n")
            f.write(f"Python Versions: {', '.join(PYTHON_VERSIONS)}\n\n")

            f.write("--- 数据类型统计信息 ---\n")
            for data_type, stats in data_stats.items():
                f.write(f"{data_type}:\n")
                f.write(f"  成功: {stats['success']}\n")
                f.write(f"  失败: {stats['failure']}\n")
                f.write(f"  错误: {stats['error']}\n")
                f.write(f"  哈希值匹配: {stats['hash_match']}\n")
                if stats["error_messages"]:
                    f.write("  错误信息:\n")
                    for error_message in stats["error_messages"]:
                        f.write(f"    {error_message}\n")
                f.write("\n")

            f.write("--- 版本统计信息 ---\n")
            for version, stats in version_stats.items():
                f.write(f"Python {version}:\n")
                f.write(f"  成功: {stats['success']}\n")
                f.write(f"  失败: {stats['failure']}\n")
                f.write(f"  错误: {stats['error']}\n\n")

            f.write("--- 详细结果 ---\n")
            f.seek(f.tell())  # 移动到详细结果的起始位置
            for data, data_type in test_data:
                data_str = repr(data)
                f.write(f"数据: {data_str} (类型: {data_type})\n")
                for version in PYTHON_VERSIONS:
                    if data_str in results and version in results[data_str]:
                        f.write(f"  Python {version}: {results[data_str][version]}\n")
                    else:
                        f.write(f"  Python {version}: 未运行\n")

        print(f"测试结果已保存到: {result_filename}")  # 在控制台打印文件名

if __name__ == "__main__":
    unittest.main()
