#!/usr/bin/env python3
"""
Скрипт для тестирования
"""

import subprocess
import json
import os

print("=" * 60)
print(" ТЕСТИРОВАНИЕ ВАРИАНТА 20")
print("=" * 60)

# 1. Тестирование SQRT
print("\n1. ТЕСТИРОВАНИЕ SQRT")
print("-" * 40)

# В run_all_tests.py, после ассемблирования test_sqrt.asm:
print("Ассемблирование test_sqrt.asm...")
result = subprocess.run(
    ["python", "assembler.py", "test_sqrt.asm", "test_sqrt.bin", "--test"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

print(result.stdout)
if result.returncode != 0:
    print("Ошибка:", result.stderr)
    # Не выходим сразу, а пробуем создать чистый файл
    print("Пробуем создать чистый файл без комментариев...")
    
    # Создаем чистую версию
    with open("test_sqrt_clean.asm", "w", encoding="utf-8") as f:
        f.write("""LOAD,1000,0
SQRT,2000,1000
LOAD,1001,1
SQRT,2001,1001
LOAD,1002,4
SQRT,2002,1002
LOAD,1003,9
SQRT,2003,1003
LOAD,1004,16
SQRT,2004,1004
LOAD,1005,25
SQRT,2005,1005
LOAD,1006,100
SQRT,2006,1006
LOAD,1007,2
SQRT,2007,1007
LOAD,1008,3
SQRT,2008,1008
LOAD,1009,10
SQRT,2009,1009
LOAD,1010,20
SQRT,2010,1010
LOAD,1011,50
SQRT,2011,1011
LOAD,1012,10000
SQRT,2012,1012
LOAD,1013,1000000
SQRT,2013,1013""")
    
    # Пробуем ассемблировать чистый файл
    result = subprocess.run(
        ["python", "assembler.py", "test_sqrt_clean.asm", "test_sqrt.bin", "--test"],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    print(result.stdout)

print("\nВыполнение программы SQRT...")
result = subprocess.run(
    ["python", "interpreter.py", "test_sqrt.json", "sqrt_dump.json", "1000", "2020"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

print(result.stdout)
if result.returncode != 0:
    print("Ошибка:", result.stderr)
    exit(1)

# Проверка результатов SQRT
if os.path.exists("sqrt_dump.json"):
    with open("sqrt_dump.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print("\nРезультаты SQRT:")
    for addr, value in sorted(data.items()):
        print(f"  {addr}: {value}")

# 2. Тестирование COPY
print("\n\n2. ТЕСТИРОВАНИЕ COPY")
print("-" * 40)

print("Ассемблирование test_copy.asm...")
result = subprocess.run(
    ["python", "assembler.py", "test_copy.asm", "test_copy.bin", "--test"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

print(result.stdout)
if result.returncode != 0:
    print("Ошибка:", result.stderr)
    exit(1)

print("\nВыполнение программы COPY...")
result = subprocess.run(
    ["python", "interpreter.py", "test_copy.json", "copy_dump.json", "5000", "8010"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

print(result.stdout)
if result.returncode != 0:
    print("Ошибка:", result.stderr)
    exit(1)

# Проверка результатов COPY
if os.path.exists("copy_dump.json"):
    with open("copy_dump.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print("\nРезультаты COPY:")
    for addr, value in sorted(data.items()):
        print(f"  {addr}: {value}")

# 3. Очистка
print("\n\n3. ОЧИСТКА")
print("-" * 40)

files_to_keep = ["test_sqrt.asm", "test_copy.asm", "assembler.py", "interpreter.py"]
files_to_remove = []

# Удаляем временные файлы
temp_files = [
    "simple_test.asm", "test.bin", "simple_test.json",
    "test_sqrt.bin", "test_sqrt.json", "sqrt_dump.json",
    "test_copy.bin", "test_copy.json", "copy_dump.json",
    "memory_dump.json"
]

for file in temp_files:
    if os.path.exists(file):
        os.remove(file)
        print(f"Удалён: {file}")

print("\n" + "=" * 60)
print(" ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 60)
