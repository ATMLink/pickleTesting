# test_inputs.py
import sys

class CustomObject:
    def __init__(self):
        self.x = 1
        self.y = "test"

TEST_INPUTS = [
    42,                     # 整型
    2**100,                # 长整型（大整数）
    3.14159,               # 浮点
    "hello",               # 字符串
    b"hello",              # 字节
    [1, 2, 3],            # 容器：列表
    {"a": 1, "b": 2},     # 容器：字典
    (1, 2),               # 容器：元组
    {1, 2, 3},           # 容器：集合
    CustomObject()         # 自定义对象
]