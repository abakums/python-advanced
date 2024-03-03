import click


@click.command()
@click.argument("filenames", required=False, nargs=-1)
def tail(filenames):
    if not filenames:
        last_17_lines = []
        try:
            while True:
                line = input()
                # Поддерживаем очередь из 17 последних строк
                last_17_lines = last_17_lines[-16:] + [line]
        except EOFError:
            print("\n".join(last_17_lines))

        return
    need_to_print_filename = len(filenames) > 1
    for i, filename in enumerate(filenames):
        if need_to_print_filename:
            # Пытался создать максимально похожий вариант утилиты:
            # начиная со второго файла перед именем файла нужен перенос строки
            if i != 0:
                print()
            print(f"==> {filename} <==")
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_lines = lines[-10:]
            for line in last_lines:
                print(line, end="")


if __name__ == "__main__":
    tail()
