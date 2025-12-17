# Configuration-Management-Practice-3
# УВМ - Вариант 20

## Описание
Реализация ассемблера и интерпретатора для учебной виртуальной машины (вариант 20).

## Файлы проекта
- `assembler.py` - ассемблер (этап 1)
- `interpreter.py` - интерпретатор (этапы 2 и 3)
- `test_sqrt.asm` - тестовая программа для SQRT
- `test_copy.asm` - тест копирования массива
- `run_all_tests.py` - скрипт тестирования

## Команды УВМ
| Команда | Формат | Описание |
|---------|--------|----------|
| LOAD | `LOAD,B,C` | `mem[B] = C` |
| READ | `READ,B,C` | `mem[B] = mem[mem[C]]` |
| WRITE | `WRITE,B,C,D` | `mem[mem[B] + D] = mem[C]` |
| SQRT | `SQRT,B,C` | `mem[B] = sqrt(mem[C])` |

## Быстрый старт
```bash
# 1. Ассемблирование
python assembler.py test_sqrt.asm test.bin --test

# 2. Выполнение
python interpreter.py test_sqrt.json dump.json 2000 2015

# 3. Полный тест
python run_all_tests.py
