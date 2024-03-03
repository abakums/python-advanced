import click


@click.command()
@click.argument("filenames", required=False, nargs=-1)
def wc(filenames):
    # Проверка наличия аргументов командной строки
    if len(filenames) < 1:
        lines = []
        try:
            while True:
                line = input()
                lines.append(f"{line}\n")
        except EOFError:
            words_count = 0
            symbols_count = 0
            for line in lines:
                words_count += len(line.split())
                symbols_count += len(line)
            print("{:>7}{:>8}{:>8}".format(len(lines), words_count, symbols_count))
        return

    # Иначе обрабатываем каждый переданный файл
    total_lines = 0
    total_words = 0
    total_symbols = 0
    for filename in filenames:
        # Открываем файл на чтение
        with open(filename, "r") as file:
            text = file.read()
            lines = text.count('\n')
            words = len(text.split())
            symbols = len(text)
            print("{:>7}{:>8}{:>8} ".format(lines, words, symbols) + filename)
            # Обновляем суммарную статистику
            total_lines += lines
            total_words += words
            total_symbols += symbols

    # Если передано больше одного файла, выводим суммарную статистику (total)
    if len(filenames) > 1:
        print("{:>7}{:>8}{:>8} ".format(total_lines, total_words, total_symbols) + "total")


if __name__ == "__main__":
    wc()
