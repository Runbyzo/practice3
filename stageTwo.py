import argparse
from stageOne import assemble_file


def encode_instruction(inst):
    result = bytearray()

    # Поле A (1 байт)
    result.append(inst["A"] & 0xFF)

    # Определяем размер аргумента в зависимости от команды
    if inst["mnemonic"] == "CONST":
        b_value = inst["B"]
        for i in range(3):
            result.append((b_value >> (8 * i)) & 0xFF)

    elif inst["mnemonic"] == "LOAD":
        b_value = inst["B"]
        for i in range(2):
            result.append((b_value >> (8 * i)) & 0xFF)

    # STORE и != не имеют аргументов в бинарном виде

    return result


def main():
    parser = argparse.ArgumentParser(description="Вариант 13, Этап 2")
    parser.add_argument("source", help="исходный .asm файл")
    parser.add_argument("output", help="выходной бинарный файл")
    parser.add_argument("--test", action="store_true", help="тестовый режим")
    args = parser.parse_args()

    instructions = assemble_file(args.source, args.test)

    if args.test:
        print("\nМашинный код:")

    binary = bytearray()

    for inst in instructions:
        encoded = encode_instruction(inst)
        binary.extend(encoded)

        if args.test:
            hex_str = ' '.join([f'0x{b:02X}' for b in encoded])
            print(f"{inst['mnemonic']} {inst['B']} -> {hex_str}")

    with open(args.output, "wb") as f:
        f.write(binary)


if __name__ == "__main__":
    main()
