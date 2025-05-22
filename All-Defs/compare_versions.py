import os

def load_results(file_path):
    results = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                try:
                    idx, result = line.strip().split(": ", 1)
                    results[idx.strip()] = result.strip()
                except ValueError:
                    continue
    return results

def compare_versions(result_files, output_path="comparison_report.txt"):
    all_keys = set()
    version_results = {}

    for version, file in result_files.items():
        results = load_results(file)
        version_results[version] = results
        all_keys.update(results.keys())

    with open(output_path, "w", encoding="utf-8") as out:
        for key in sorted(all_keys, key=lambda x: int(x[1:])):  # sort by test number
            line = f"{key}:"
            statuses = []
            for version in result_files:
                status = version_results[version].get(key, "missing")
                statuses.append(f"{version}={status}")
            if len(set(statuses)) > 1:
                out.write(f"{key}: {' | '.join(statuses)}\n")

if __name__ == "__main__":
    # 修改为你各版本的输出文件路径
    result_files = {
        "py3.7": "data_py37.out",
        "py3.8": "data_py38.out",
        "py3.9": "data_py39.out",
    }
    compare_versions(result_files)
