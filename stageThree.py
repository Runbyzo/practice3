import argparse

# Таблица размеров команд
SIZES = {
    6: 4,  # CONST
    2: 2,  # LOAD
    4: 4,  # STORE
    7: 2,  # !=
}

class UVM:
    def __init__(self, memory_size=256):
        self.MEM = [0] * memory_size
        self.PC = 0
        self.STACK = []
        self.commands_executed = 0

    def load_binary(self, filename):
        with open(filename, "rb") as f:
            code = f.read()
        for i, byte in enumerate(code):
            self.MEM[i] = byte

    def fetch(self):
        return self.MEM[self.PC]

    def decode_and_execute(self):
        if self.PC >= len(self.MEM):
            return

        opcode = self.fetch()
        print(f"[DEBUG] PC={self.PC}, opcode={opcode}, stack={self.STACK}")

        if opcode == 0:  # Конец программы
            self.PC += 1
            return

        self.PC += 1
        self.commands_executed += 1

        # 1. Загрузка константы (A=6) - 4 байта всего
        if opcode == 6:
            const = 0
            for i in range(3):
                const |= self.MEM[self.PC + i] << (8 * i)
            self.PC += 3
            self.STACK.append(const)
            print(f"  → CONST {const} pushed to stack")

        # 2. Чтение из памяти (A=2) - 3 байта всего
        elif opcode == 2:
            addr = 0
            for i in range(2):
                addr |= self.MEM[self.PC + i] << (8 * i)
            self.PC += 2

            # Проверяем границы
            if addr >= len(self.MEM):
                print(f"  → ERROR: Address {addr} out of bounds")
                self.STACK.append(0)
            else:
                value = self.MEM[addr]
                self.STACK.append(value)
                print(f"  → LOAD from addr {addr} = {value}")

        # 3. Запись в память (A=4) - 1 байт
        elif opcode == 4:
            if len(self.STACK) < 2:
                print(f"  → WARNING: Stack underflow for STORE")
                return
            addr = self.STACK.pop()
            value = self.STACK.pop()

            if addr >= len(self.MEM):
                print(f"  → ERROR: Address {addr} out of bounds for STORE")
            else:
                self.MEM[addr] = value
                print(f"  → STORE value {value} to addr {addr}")

        # 4. Операция "!=" (A=7) - 1 байт
        elif opcode == 7:
            if len(self.STACK) < 2:
                print(f"  → WARNING: Stack underflow for !=")
                return

            value2 = self.STACK.pop()
            value1 = self.STACK.pop()

            result = 1 if value1 != value2 else 0
            self.STACK.append(result)
            print(f"  → != : {value1} != {value2} = {result}")

        else:
            print(f"  → ERROR: Unknown opcode {opcode}")
            return

    def run(self):
        while self.PC < len(self.MEM):
            current_pc = self.PC
            self.decode_and_execute()

            # Если PC не изменился, значит произошла ошибка
            if self.PC == current_pc:
                print(f"[ERROR] Program stuck at PC={self.PC}")
                break

        print(f"[INFO] Program finished. Commands executed: {self.commands_executed}")
        print(f"[INFO] Final stack: {self.STACK}")

def main():
    parser = argparse.ArgumentParser(description="УВМ")
    parser.add_argument("binary", help="бинарный файл")
    args = parser.parse_args()

    vm = UVM(memory_size=256)
    vm.load_binary(args.binary)
    vm.run()

if __name__ == "__main__":
    main()













# Покажем состояние стека в конце
    #print(f"Состояние стека: {vm.STACK}")
    # Покажем первые 20 ячеек памяти
    #print("Первые 20 ячеек памяти:", vm.MEM[:20])
