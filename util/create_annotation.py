import pandas as pd

def create_annotation(filename: str, result_folder: str):
    """Create annotation for a given dataset

    Args:
        filename: path to the dataset
        result_folder: path to the folder where annotation file will be stored
    Returns:
        True on success
    """
    df = pd.read_csv(filename, sep=";")
    annotation_file = open(result_folder + "/annotation.txt", "w+")
    annotation_file.write("Путь до файла: " + filename + "\n")
    annotation_file.write("Количество строк: " + str(len(df.index)) + "\n")
    annotation_file.write("Типы столбцов:\n" + str(df.dtypes) + "\n")
    annotation_file.close()
    return True

def main():
    print("Введите путь до файла (./dataset.csv): ", end="")
    filename = input()
    if filename.strip() == "":
        filename = "./dataset.csv"
    
    print("Введите путь до папки, куда будет сохранён файл аннотации (./): ", end="")
    result_folder = input()
    if result_folder.strip() == "":
        result_folder = "./"

    if create_annotation(filename=filename, result_folder=result_folder):
        print("Успех")
    else:
        print("Провал")
    
if __name__ == '__main__':
    main()
