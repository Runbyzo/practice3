import argparse

OPCODES = {
    "CONST": 6,
    "LOAD": 2,
    "STORE": 4,
    "!=": 7,
}

#размеры команд в байтах
SIZES = {
    "CONST": 4,
    "LOAD": 3,
    "STORE": 1,
    "!=": 1,
}

# Команды без аргументов в исходном коде
NO_ARG_COMMANDS = {"STORE", "!="}

def strip_comment(line: str) -> str:
    if ";" in line:
        line = line.split(";", 1)[0]
    return line.strip()


def parse_line(line: str):
    line = strip_comment(line)
    if not line:
        return None

    parts = line.split()
    if not parts:
        return None

    mnemonic = parts[0].upper()

    if mnemonic not in OPCODES:
        raise ValueError(f"Неизвестная команда: {mnemonic}")

    # Определяем, какие команды требуют аргументов
    if mnemonic in ["CONST", "LOAD"]:
        # CONST и LOAD требуют аргумент
        if len(parts) != 2:
            raise ValueError(f"{mnemonic}: ожидается один аргумент")
        value = int(parts[1], 0)
    elif mnemonic in ["STORE", "!="]:
        # STORE и != не требуют аргументов
        if len(parts) > 1:
            # Предупреждение, но не ошибка
            if test_mode:  # если нужно только для тестового режима
                print(f"[WARNING] {mnemonic} не принимает аргументов, игнорирую '{parts[1]}'")
        value = 0  # фиктивное значение
    else:
        value = 0

    inst = {
        "mnemonic": mnemonic,
        "A": OPCODES[mnemonic],
        "B": value,
    }

    return inst

def assemble_file(source_path, test=False):
    instructions = []

    with open(source_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                inst = parse_line(line)
                if inst:
                    instructions.append(inst)
            except ValueError as e:
                print(f"Ошибка в строке {line_num}: {e}")
                print(f"  Строка: '{line.strip()}'")
                return None
            except Exception as e:
                print(f"Неожиданная ошибка в строке {line_num}: {e}")
                print(f"  Строка: '{line.strip()}'")
                return None

    if test:
        print("\nПромежуточное представление:")
        for inst in instructions:
            print(f"{inst['mnemonic']}: A={inst['A']}, B={inst['B']}")

    return instructions


def main():
    parser = argparse.ArgumentParser(description="Вариант 13, Этап 1 (исправленный)")
    parser.add_argument("source", help="исходный .asm файл")
    parser.add_argument("--test", action="store_true", help="тестовый режим")
    args = parser.parse_args()

    assemble_file(args.source, args.test)


if __name__ == "__main__":
    main()
