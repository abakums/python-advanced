# собираем latex в списке в качестве оптимизации -- если конкатенировать строки (а не добавлять их в список),
# то при каждой операции конкатенации будет создаваться новая строка, так как строки неизменяемые -> это может
# быть неэффективно при большом числе строк
def generate_latex_template(line: str | list[str], *args):
    """
    Передается либо строки latex, к которым нужно добавить шаблонные инструкции latex, либо список строк (line)
    :param line: либо первая строка из переданных, либо список всех строк
    :param args: оставшиеся строки, если line -- строка
    :return: валидный latex
    """
    result = [
        "\\documentclass{article}\n",
        "\\usepackage{graphicx}\n",
        "\\usepackage{grffile}\n"
        "\\begin{document}\n",
    ]
    if isinstance(line, str):
        result.append(line)
        if args:
            result += args
    elif isinstance(line, list):
        result.extend(line)
    result.append("\\end{document}\n")
    return "".join(result)


def generate_latex_table(data: list[list[str]]):
    """
    Функция для генерации таблицы latex без шаблонных инструкций начала и конца документа
    :param data: список строк таблицы
    :return: latex без шаблонных инструкций
    """
    if not data:
        return ""

    num_cols = max([len(row) for row in data])
    table = ["\\begin{tabular}{|" + "c|" * num_cols + "}\n", "\\hline\n"]

    for row in data:
        table.append(" & ".join(str(cell) for cell in row))
        table.append(" \\\\\n")
        table.append("\\hline\n")

    table.append("\\end{tabular} \\\\\n")

    return "".join(table)


def generate_latex_image(image_path: str, picture_width: int | float = 1):
    """
    Функция для генерации таблицы latex без шаблонных инструкций начала и конца документа

    :param image_path: путь до изображения
    :param picture_width: ширина изображения (int | float)
    :return: latex без шаблонных инструкций
    """
    data = [f"\\includegraphics[width={picture_width}\\textwidth]{{{image_path}}}\n"]

    return "".join(data)
