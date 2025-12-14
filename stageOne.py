import argparse

OPCODES = {
    "CONST": 145,    # загрузка константы в аккумулятор
    "LOAD": 193,     # чтение значения из памяти
    "STORE": 201,    # запись значения в память
    "NEG": 161,      # унарная операция отрицания
}

SIZES = {
    "CONST": 3,
    "LOAD": 4,
    "STORE": 4,
    "NEG": 2,
}


def strip_comment(line: str) -> str:
    #Поддержка комментариев начинающихся с ";"

    if ";" in line:
        line = line.split(";", 1)[0]
    return line.strip()


def parse_line(line: str):
    #Разбор строки ассемблера в элемент IR.

    line = strip_comment(line)
    if not line:
        return None

    parts = line.split()
    mnemonic = parts[0].upper()

    if mnemonic not in OPCODES:
        raise ValueError(f"Неизвестная команда: {mnemonic}")

    if len(parts) != 2:
        raise ValueError(f"{mnemonic}: ожидается один аргумент")

    value = int(parts[1], 0)

    # Промежуточное представление (элемент IR)

    inst = {
        "mnemonic": mnemonic,
        "A": OPCODES[mnemonic],
        "B": value,
        "size": SIZES[mnemonic],
    }

    return inst


def main():
    parser = argparse.ArgumentParser(
        description="Вариант13, Этап1"
    )
    parser.add_argument("source", help="исходный .asm файл")
    parser.add_argument(
        "--test",
        action="store_true",
        help="выведите поля A,B для каждой команды",
    )
    args = parser.parse_args()

    instructions = []

    with open(args.source, "r", encoding="utf-8") as f:
        for line in f:
            inst = parse_line(line)
            if inst:
                instructions.append(inst)

    # Тестовый режим — вывод A,B
    if args.test:
        for inst in instructions:
            print(f"A={inst['A']}, B={inst['B']}")

    return instructions


if __name__ == "__main__":
    main()
