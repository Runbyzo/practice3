
from stageOne import main as assemble_to_ir


def encode_instruction(inst):
    #Кодирование одной IR-инструкции в байты УВМ
    result = bytearray()

    # Поле A (1 байт)
    result.append(inst["A"] & 0xFF)

    # Поле B (size - 1 байт)
    b_size = inst["size"] - 1
    b_value = inst["B"]

    for i in reversed(range(b_size)):
        result.append((b_value >> (8 * i)) & 0xFF)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Вариант 13, Этап 2"
    )
    parser.add_argument("source", help="исходный .asm файл")
    parser.add_argument("output", help="выходной бинарный файл")
    args = parser.parse_args()

    # IR
    instructions = assemble_to_ir()

    binary = bytearray()

    # машинный код
    for inst in instructions:
        binary.extend(encode_instruction(inst))

    # Запись двоичного файла
    with open(args.output, "wb") as f:
        f.write(binary)


if __name__ == "__main__":
    main()
