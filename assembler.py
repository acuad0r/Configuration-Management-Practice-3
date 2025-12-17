import sys
import json

# Спецификация команд УВМ (вариант 20)
CMD_SPECS = {
    "LOAD": {"opcode": 72, "size": 11, "fields": ["B", "C"]},
    "READ": {"opcode": 226, "size": 11, "fields": ["B", "C"]},
    "WRITE": {"opcode": 75, "size": 11, "fields": ["B", "C", "D"]},
    "SQRT": {"opcode": 24, "size": 11, "fields": ["B", "C"]}
}

def parse_line(line):
    """Парсит строку CSV формата"""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    
    parts = [p.strip() for p in line.split(",")]
    mnemonic = parts[0].upper()
    
    if mnemonic not in CMD_SPECS:
        raise ValueError(f"Неизвестная команда: {mnemonic}")
    
    # Преобразуем аргументы в числа
    args = []
    for part in parts[1:]:
        if part.startswith("0x"):
            args.append(int(part, 16))
        else:
            args.append(int(part))
    
    return {"mnemonic": mnemonic, "args": args}

def assemble(source_path, output_bin_path, test_mode=False):
    """Основная функция ассемблирования"""
    
    instructions = []
    
    # Чтение исходного файла с указанием кодировки
    with open(source_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                inst = parse_line(line)
                if inst:
                    # Проверка количества аргументов
                    expected = len(CMD_SPECS[inst["mnemonic"]]["fields"])
                    if len(inst["args"]) != expected:
                        raise ValueError(f"Неверное число аргументов для {inst['mnemonic']}")
                    instructions.append(inst)
            except Exception as e:
                print(f"Ошибка в строке {line_num}: {e}")
                if not test_mode:
                    raise
    
    # Сохраняем промежуточное представление (JSON)
    intermediate = {
        "instructions": instructions,
        "metadata": {
            "source": source_path,
            "command_count": len(instructions),
            "variant": 20
        }
    }
    
    intermediate_path = output_bin_path.replace(".bin", ".json")
    with open(intermediate_path, "w", encoding="utf-8") as f:
        json.dump(intermediate, f, indent=2)
    
    # Создаем бинарный файл (упрощенно)
    with open(output_bin_path, "wb") as f:
        # Записываем количество команд
        f.write(len(instructions).to_bytes(4, 'little'))
        
        for inst in instructions:
            opcode = CMD_SPECS[inst["mnemonic"]]["opcode"]
            f.write(opcode.to_bytes(1, 'little'))
            
            for arg in inst["args"]:
                f.write(arg.to_bytes(4, 'little'))
            
            # Дополняем до 11 байт
            bytes_written = 1 + len(inst["args"]) * 4
            f.write(b"\x00" * (11 - bytes_written))
    
    # Режим тестирования
    if test_mode:
        print("\n=== ВНУТРЕННЕЕ ПРЕДСТАВЛЕНИЕ ===")
        for idx, inst in enumerate(instructions):
            print(f"{idx:3d}: {inst['mnemonic']:8} {inst['args']}")
        print(f"=== Всего команд: {len(instructions)} ===")
    
    print(f"✓ Ассемблирование завершено")
    print(f"  - Файл: {intermediate_path}")
    return intermediate_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Использование: python assembler.py <input.asm> <output.bin> [--test]")
        print("Пример: python assembler.py test_sqrt.asm test.bin --test")
        sys.exit(1)
    
    source = sys.argv[1]
    output = sys.argv[2]
    test_mode = "--test" in sys.argv
    
    try:
        assemble(source, output, test_mode)
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        sys.exit(1)
