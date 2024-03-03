import click


def print_format_line(line_number_before: int, ba: bool, line: str) -> int:
    line = line.strip()
    # add_number обозначает, нужно ли на текущей итерации добавлять номер строки и выводить ее
    add_number = ba or (not ba and line)
    if add_number:
        print(f"{line_number_before}".rjust(6), end="  ")
    # строку вводим всегда, если она пустая -- этот print работает как перенос строки (как в оригинале nl)
    print(line)
    if add_number:
        return line_number_before + 1
    return line_number_before


@click.command()
@click.option("-ba", is_flag=True, default=False, help="Для учета пустых строк")
@click.argument("filename", required=False)
def nl(ba, filename):
    line_number = 1
    if filename:
        with open(filename, "r") as f:
            for line in f:
                line_number = print_format_line(line_number, ba, line)
        return

    try:
        while True:
            line = input()
            line_number = print_format_line(line_number, ba, line)
    except EOFError:
        print("Остановка ввода")


if __name__ == "__main__":
    nl()
