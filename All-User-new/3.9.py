{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "ec812686-af20-411b-8581-717f35537663",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[+] Written 'pickle_p4_py3.9.json'\n"
     ]
    }
   ],
   "source": [
    "# pickle_all_uses_test.py\n",
    "\n",
    "import sys\n",
    "import pickle\n",
    "import hashlib\n",
    "import datetime\n",
    "import os\n",
    "from collections import namedtuple\n",
    "\n",
    "# -----------------------\n",
    "# —— 在此处定义所有测试对象 —— #\n",
    "# 定义点必须是模块顶层，保证 pickle 能找到它们\n",
    "# -----------------------\n",
    "Point = namedtuple('Point', ['x', 'y'])\n",
    "\n",
    "class CustomObject:\n",
    "    def __init__(self, name, value):\n",
    "        self.name = name\n",
    "        self.value = value\n",
    "    def __str__(self):\n",
    "        # 包含字段，序列化后字段应保持一致\n",
    "        return f\"<CustomObject name={self.name!r} value={self.value!r}>\"\n",
    "\n",
    "def top_level_func(a, b=5):\n",
    "    return a + b\n",
    "\n",
    "# 所有测试输入 — 覆盖各定义点的使用\n",
    "TEST_INPUTS = [\n",
    "    42,                             # int\n",
    "    2**100,                         # 大整数\n",
    "    3.14159,                        # float\n",
    "    \"hello\",                      # str\n",
    "    b\"hello\",                     # bytes\n",
    "    [1, 2, 3],                      # list\n",
    "    {\"a\": 1, \"b\": 2},           # dict\n",
    "    (1, 2),                         # tuple\n",
    "    {1, 2, 3},                      # set\n",
    "    frozenset([4, 5, 6]),           # frozenset\n",
    "    range(5),                       # range\n",
    "    Point(5, 6),                    # namedtuple\n",
    "    CustomObject(\"foo\", 123),     # 自定义对象\n",
    "    top_level_func,                 # 顶层函数\n",
    "]\n",
    "\n",
    "# ---- 配置 ----\n",
    "# 可以自定义输出文件夹和文件名\n",
    "OUTPUT_FOLDER = 'data'               # 输出文件夹名称\n",
    "OUTPUT_FILENAME = '3.9test_results.txt' # 输出文件名，可修改为任意名称\n",
    "\n",
    "# ---- 辅助函数 ----\n",
    "def sha256_of_str(obj):\n",
    "    \"\"\"对 str(obj) 的 UTF8 编码做 SHA-256，返回 hex.\"\"\"\n",
    "    return hashlib.sha256(str(obj).encode('utf-8')).hexdigest()\n",
    "\n",
    "def test_obj(obj):\n",
    "    orig_hash = sha256_of_str(obj)\n",
    "    dumped = pickle.dumps(obj, protocol=4)\n",
    "    loaded = pickle.loads(dumped)\n",
    "    loaded_hash = sha256_of_str(loaded)\n",
    "    return orig_hash, loaded_hash, (orig_hash == loaded_hash)\n",
    "\n",
    "# ---- 主逻辑 ----\n",
    "def main():\n",
    "    # 确保输出目录存在\n",
    "    output_dir = os.path.join(os.getcwd(), OUTPUT_FOLDER)\n",
    "    os.makedirs(output_dir, exist_ok=True)\n",
    "\n",
    "    # 如果使用默认 OUTPUT_FILENAME，则在文件名前加 Python 版本后缀\n",
    "    py_ver = f\"_py{sys.version_info.major}{sys.version_info.minor}\"\n",
    "    name, ext = os.path.splitext(OUTPUT_FILENAME)\n",
    "    outfile = os.path.join(output_dir, f\"{name}{py_ver}{ext}\")\n",
    "\n",
    "    with open(outfile, 'w', encoding='utf-8') as f:\n",
    "        def writeline(line=''):\n",
    "            print(line)\n",
    "            f.write(line + '\\n')\n",
    "\n",
    "        writeline(f\"Python version: {sys.version.strip()}\")\n",
    "        writeline(f\"Test time: {datetime.datetime.now()!s}\")\n",
    "        writeline(\"=== Pickle Test Output ===\")\n",
    "        writeline()\n",
    "        for obj in TEST_INPUTS:\n",
    "            orig_h, load_h, match = test_obj(obj)\n",
    "            writeline(f\"Input: {obj!s}\")\n",
    "            writeline(f\"Original object hash:    {orig_h}\")\n",
    "            writeline(f\"Deserialized object hash: {load_h}\")\n",
    "            writeline(f\"Match: {match}\")\n",
    "            writeline()\n",
    "\n",
    "    print(f\"[+] Results saved to {outfile}\")\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    main()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b5b96ae0-5eaf-4394-bf90-cf1aba72e372",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3.9",
   "language": "python",
   "name": "py39"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.21"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
