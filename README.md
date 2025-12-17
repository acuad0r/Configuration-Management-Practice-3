# Configuration-Management-Practice-3
# УВМ Вариант №20

## Описание
Реализация ассемблера и интерпретатора для учебной виртуальной машины (вариант 20).

## Команды УВМ
1. `LOAD B C` — загрузить константу C по адресу B
2. `READ B C` — прочитать из памяти: mem[B] = mem[mem[C]]
3. `WRITE B C D` — записать в память: mem[mem[B] + D] = mem[C]
4. `SQRT B C` — квадратный корень: mem[B] = sqrt(mem[C])

## Запуск
1. Ассемблирование:
   ```bash
   python assembler.py program.asm program.bin --test
