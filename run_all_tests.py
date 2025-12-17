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

# 1. Ассемблирование
print("\n1. АССЕМБЛИРОВАНИЕ")
print("-" * 40)

# Создаем простую тестовую программу
test_program = """# Простая тестовая программа
LOAD,1000,25
SQRT,1001,1000
LOAD,1002,100
SQRT,1003,1002
"""

with open("simple_test.asm", "w", encoding="utf-8") as f:
    f.write(test_program)

print("Создана программа simple_test.asm")

# Запускаем ассемблер
print("Запуск ассемблера...")
result = subprocess.run(
    ["python", "assembler.py", "simple_test.asm", "test.bin", "--test"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

print(result.stdout)
if result.returncode != 0:
    print("Ошибка:", result.stderr)
    exit(1)

# 2. Выполнение
print("\n2. ВЫПОЛНЕНИЕ ПРОГРАММЫ")
print("-" * 40)

print("Запуск интерпретатора...")
result = subprocess.run(
    ["python", "interpreter.py", "test.json", "memory_dump.json", "1000", "1010"],
    capture_output=True,
    text=True,
    encoding="utf-8"
)

print(result.stdout)
if result.returncode != 0:
    print("Ошибка:", result.stderr)
    exit(1)

# 3. Проверка результатов
print("\n3. ПРОВЕРКА РЕЗУЛЬТАТОВ")
print("-" * 40)

if os.path.exists("memory_dump.json"):
    with open("memory_dump.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    print("Содержимое дампа памяти:")
    for addr, value in sorted(data.items()):
        print(f"  {addr}: {value}")
    
    # Проверяем конкретные значения
    print("\nПроверка вычислений:")
    print("-" * 30)
    
    expected_results = [
        ("0x3e8", 25, "Исходное значение 25"),
        ("0x3e9", 5, "sqrt(25) = 5"),
        ("0x3ea", 100, "Исходное значение 100"),
        ("0x3eb", 10, "sqrt(100) = 10")
    ]
    
    all_correct = True
    for addr, expected, description in expected_results:
        if addr in data:
            actual = data[addr]
            if actual == expected:
                print(f"✓ {addr}: {actual} - {description}")
            else:
                print(f"✗ {addr}: {actual} (ожидалось {expected}) - {description}")
                all_correct = False
        else:
            print(f"✗ {addr}: не найден - {description}")
            all_correct = False
    
    if all_correct:
        print("\n" + "=" * 60)
        print(" ✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print(" ⚠ ЕСТЬ ОШИБКИ В ВЫЧИСЛЕНИЯХ")
        print("=" * 60)
    
    # Показываем состояние памяти
    print("\nСостояние памяти (адреса 1000-1010):")
    for addr in range(1000, 1010):
        hex_addr = hex(addr)
        if hex_addr in data:
            print(f"  mem[{addr}] = {data[hex_addr]}")
else:
    print("Файл memory_dump.json не найден")

# Очистка
print("\n4. ОЧИСТКА")
print("-" * 40)
files_to_remove = ["simple_test.asm", "test.bin", "simple_test.json", "memory_dump.json"]
for file in files_to_remove:
    if os.path.exists(file):
        os.remove(file)
        print(f"Удалён: {file}")

print("\n" + "=" * 60)
print(" ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 60)
