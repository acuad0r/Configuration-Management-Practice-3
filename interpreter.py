import sys
import json
import math

class UVM:
    def __init__(self, mem_size=65536):
        """Инициализация виртуальной машины"""
        self.memory = [0] * mem_size
    
    def load_constant(self, B, C):
        """LOAD B C: mem[B] = C"""
        self.memory[B] = C
    
    def read_memory(self, B, C):
        """READ B C: mem[B] = mem[mem[C]]"""
        addr = self.memory[C]
        self.memory[B] = self.memory[addr]
    
    def write_memory(self, B, C, D):
        """WRITE B C D: mem[mem[B] + D] = mem[C]"""
        base_addr = self.memory[B]
        target_addr = base_addr + D
        self.memory[target_addr] = self.memory[C]
    
    def sqrt_operation(self, B, C):
        """SQRT B C: mem[B] = sqrt(mem[C]) (целочисленный корень)"""
        value = self.memory[C]
        if value < 0:
            result = 0
        else:
            result = int(math.sqrt(value))  # Округляем вниз
        self.memory[B] = result
        print(f"[SQRT] sqrt({value}) = {result} -> mem[{B}]")
    
    def execute(self, instructions):
        """Выполнение списка инструкций"""
        for inst in instructions:
            op = inst["mnemonic"]
            args = inst["args"]
            
            if op == "LOAD":
                self.load_constant(args[0], args[1])
            elif op == "READ":
                self.read_memory(args[0], args[1])
            elif op == "WRITE":
                self.write_memory(args[0], args[1], args[2])
            elif op == "SQRT":
                self.sqrt_operation(args[0], args[1])
            else:
                print(f"Неизвестная команда: {op}")
    
    def dump_memory(self, start, end):
        """Создание дампа памяти в JSON формате"""
        dump = {}
        for addr in range(start, min(end, len(self.memory))):
            value = self.memory[addr]
            if value != 0:
                dump[hex(addr)] = value
        return json.dumps(dump, indent=2)

def run_interpreter(intermediate_path, dump_path, range_start, range_end):
    """Запуск интерпретатора"""
    print(f"Запуск интерпретатора УВМ")
    
    # Загрузка промежуточного представления
    with open(intermediate_path, "r") as f:
        data = json.load(f)
    
    # Проверка структуры
    if "instructions" not in data:
        print("Ошибка: некорректный формат файла")
        return
    
    # Создание и запуск ВМ
    uvm = UVM()
    uvm.execute(data["instructions"])
    
    # Создание дампа
    dump = uvm.dump_memory(range_start, range_end)
    
    # Сохранение дампа
    with open(dump_path, "w") as f:
        f.write(dump)
    
    print(f"Выполнение завершено")
    print(f"Дамп сохранён в {dump_path}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Использование: python interpreter.py <intermediate.json> <dump.json> <start> <end>")
        sys.exit(1)
    
    intermediate = sys.argv[1]
    dump = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    
    run_interpreter(intermediate, dump, start, end)