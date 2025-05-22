@echo off

cd /d "G:\SoftwareTest\pickleTesting\All-Defs"

echo Running Python 3.7...
"G:\SoftwareTest\pickleTesting\env_3.7\Scripts\python.exe" run_pickle_fuzz_tests.py
rename data.in data_py37.in
rename data.out data_py37.out

echo Running Python 3.8...
"G:\SoftwareTest\pickleTesting\env_3.8\Scripts\python.exe" run_pickle_fuzz_tests.py
rename data.in data_py38.in
rename data.out data_py38.out

echo Running Python 3.9...
"G:\SoftwareTest\pickleTesting\env_3.9\Scripts\python.exe" run_pickle_fuzz_tests.py
rename data.in data_py39.in
rename data.out data_py39.out

echo Comparing results...
"G:\SoftwareTest\pickleTesting\env_3.9\Scripts\python.exe" compare_versions.py

echo All done.
pause
