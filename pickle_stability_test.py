import pickle
import hashlib
import sys

print(f"运行于 Python {sys.version}")

class CustomObject:
    def __init__(self, value):
        self.value = value

test_objects = [
    0, 1, -1, 2**64 - 1,  # 整数
    0.0, 1.0, -1.0, 1e100, float('inf'), float('nan'),  # 浮点数
    "", "hello", "café",  # 字符串
    [], [1, 2], [[1], [2]],  # 列表
    (), (1,), (1, 2, 3),  # 元组
    {}, {1: "one"}, {"a": 1, "b": 2},  # 字典
    set(), {1, 2, 3},  # 集合
    CustomObject(42),  # 自定义对象
    [1, 2, [3]],  # 递归结构
]

# 添加递归列表
recursive_list = [1, 2, 3]
recursive_list.append(recursive_list)
test_objects.append(recursive_list)

hashes = {}
for obj in test_objects:
    pickled = pickle.dumps(obj, protocol=4)
    hash_value = hashlib.sha256(pickled).hexdigest()
    hashes[repr(obj)] = hash_value

output_file = f"pickle_hashes_{sys.version_info.major}.{sys.version_info.minor}.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for obj, hash_value in hashes.items():
        f.write(f"{obj}: {hash_value}\n")

print(f"测试完成，结果已保存到 {output_file}")