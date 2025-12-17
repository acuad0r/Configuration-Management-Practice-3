#!/usr/bin/env python3
"""
Скрипт для тестирования всех этапов проекта
"""

import subprocess
import os
import json

def print_step(step_name):
    """Красивый вывод шага"""
    print("\n" + "="*60)
    print(f" {step_name}")
    print("="*60)

def run_command(cmd):
    """Запуск команды"""
    print(f"Выполняю: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Успешно")
        if result.stdout:
            print(result.stdout[:200])  # Первые 200 символов
    else:
        print("✗ Ошибка")
        if result.stderr:
            print(result.stderr)
    
    return result.returncode == 0

def main():
    """Основная функция тестирования"""
    print("="*60)
    print(" ПОЛНОЕ ТЕСТИРОВАНИЕ ВАРИАНТА 20")
    print("="*60)
    
    # Проверяем существование файлов
    required_files = ["assembler.py", "interpreter.py", "test_sqrt.asm"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"✗ Файл {file} не найден!")
            return
    
    # === ЭТАП 1: Ассемблирование ===
    print_step("ЭТАП 1: Ассемблирование")
    
    # Ассемблируем тестовую программу SQRT
    success = run_command([
        "python", "assembler.py", 
        "test_sqrt.asm", 
        "test_sqrt.bin", 
        "--test"
    ])
    
    if not success:
        print("✗ Этап 1 не пройден")
        return
    
    # === ЭТАП 2 и 3: Интерпретация ===
    print_step("ЭТАП 2-3: Выполнение и проверка SQRT")
    
    # Выполняем программу
    success = run_command([
        "python", "interpreter.py",
        "test_sqrt.json",
        "memory_dump.json",
        "2000", "2015"  # Смотрим адреса результатов
    ])
    
    if not success:
        print("✗ Этапы 2-3 не пройдены")
        return
    
    # === ПРОВЕРКА РЕЗУЛЬТАТОВ ===
    print_step("ПРОВЕРКА РЕЗУЛЬТАТОВ")
    
    if os.path.exists("memory_dump.json"):
        with open("memory_dump.json", "r") as f:
            dump = json.load(f)
        
        # Ожидаемые результаты для адресов 2000-2006
        expected = {
            2000: 0,    # sqrt(0)
            2001: 1,    # sqrt(1)
            2002: 2,    # sqrt(4)
            2003: 3,    # sqrt(9)
            2004: 4,    # sqrt(16)
            2005: 5,    # sqrt(25)
            2006: 10,   # sqrt(100)
        }
        
        print("\nПроверка вычислений SQRT:")
        print("-" * 40)
        
        all_correct = True
        for addr, expected_value in expected.items():
            hex_addr = hex(addr)
            if hex_addr in dump:
                actual = dump[hex_addr]
                status = "✓" if actual == expected_value else "✗"
                print(f"{status} mem[{addr}] = {actual} (ожидалось {expected_value})")
                if actual != expected_value:
                    all_correct = False
            else:
                print(f"✗ mem[{addr}] не найден в дампе")
                all_correct = False
        
        if all_correct:
            print("\nВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        else:
            print("\nНЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ")
        
        # Показываем полный дамп
        print(f"\nПолный дамп ({len(dump)} значений):")
        for addr, value in dump.items():
            print(f"  {addr}: {value}")
    
    else:
        print("Файл дампа не создан")
    
    print("\n" + "="*60)
    print(" ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("="*60)

if __name__ == "__main__":
    main()