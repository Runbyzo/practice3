import argparse

# Таблица размеров команд
SIZES = {
    145: 3,  # CONST
    193: 4,  # LOAD
    201: 4,  # STORE
    161: 2,  # NEG
}


class UVM:
    def __init__(self, memory_size=256):
        self.ACC = 0
        self.PC = 0
        self.MEM = [0] * memory_size
        self.CODE = bytearray()

    def load_program(self, filename):
        with open(filename, "rb") as f:
            self.CODE = bytearray(f.read())

    def fetch(self):
        return self.CODE[self.PC]

    def decode_argument(self, size):
        b_size = size - 1
        value = 0
        for i in range(b_size):
            value = (value << 8) | self.CODE[self.PC + 1 + i]
        return value

    def step(self):
        opcode = self.fetch()
        size = SIZES[opcode]
        arg = self.decode_argument(size)

        # Выполнение команды
        if opcode == 145:          # CONST
            self.ACC = arg

        elif opcode == 193:        # LOAD
            self.ACC = self.MEM[arg]

        elif opcode == 201:        # STORE
            self.MEM[arg] = self.ACC

        elif opcode == 161:        # NEG
            self.ACC = -self.ACC

        else:
            raise RuntimeError(f"Неизвестный код операции: {opcode}")

        self.PC += size

    def run(self):
        while self.PC < len(self.CODE):
            self.step()


def main():
    parser = argparse.ArgumentParser(
        description="Вариант 13, Этап 3"
    )
    parser.add_argument("binary", help="двоичный файл программы")
    args = parser.parse_args()

    vm = UVM()
    vm.load_program(args.binary)
    vm.run()

    # Итоговое состояние 
    print(f"ACC = {vm.ACC}")


if __name__ == "__main__":
    main()
