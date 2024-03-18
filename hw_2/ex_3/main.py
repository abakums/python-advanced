from my_latex_package.latex_functions import generate_latex_table, generate_latex_image, generate_latex_template


if __name__ == "__main__":
    picture_path = "images/test.png"

    data = [
        ["Name", "Age", "City"],
        ["User1", 20, "New York"],
        ["User2", 21, "Los Angeles"],
        ["User3", 22, "Chicago"]
    ]
    latex_table = generate_latex_table(data)
    latex_image = generate_latex_image(picture_path)
    latex_document = generate_latex_template(latex_table, latex_image)
    with open("output.tex", "w") as file:
        file.write(latex_document)
