# test_inputs.py
import sys

class CustomObject:
    def __init__(self):
        self.x = 1
        self.y = "test"

class CustomGetState:
    def __init__(self):
        self.a = 10
    def __getstate__(self):
        return {"state": self.a}

def dummy_function(x): return x

TEST_INPUTS = [
    # None 和布尔类型
    None,
    True, False,

    # 数字类型
    0, 42, -1,
    2**100,
    3.14159, -0.1,
    3 + 4j,

    # 字符串和字节
    "", "hello", "你好", "😊",
    b"hello", bytearray(b"world"),

    # 容器类型
    [], [1, 2, 3], [1, [2, 3]], [1, "a", None],
    (), (1,), (1, 2), (1, "a", None),
    {}, {"a": 1, "b": {"c": 2}},
    set(), {1, 2, 3}, frozenset({4, 5}),

    # 自定义对象
    CustomObject(),
    CustomGetState(),

    # 异常对象
    ValueError("Test error"),

    # 特殊对象
    ..., NotImplemented,

    # 不可pickle的（用于测试异常处理）
    dummy_function,   # 会报错
    sys               # 会报错
]