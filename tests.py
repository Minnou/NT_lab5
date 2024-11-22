import unittest
import os
from util import make_x_y, find_value, split_by_week, split_by_year, data_analysis
import pandas as pd

class TestMakeXY(unittest.TestCase):
    def setUp(self):
        """Создание тестовых файлов перед запуском каждого теста."""
        # Создаем тестовый файл с корректными данными
        self.test_dataset = "./test_dataset_xy.csv"
        with open(self.test_dataset, "w+") as f:
            f.write("2023-10-01;100\n2023-10-02;200\n2023-10-03;300\n")
        
        # Пустой файл для тестов
        self.empty_file = "./empty.csv"
        open(self.empty_file, "w+").close()
        
        # Файлы для результатов
        self.test_x_file = "./test_x.csv"
        self.test_y_file = "./test_y.csv"

    def tearDown(self):
        """Удаление всех созданных файлов после каждого теста."""
        for file in [self.test_dataset, self.empty_file, self.test_x_file, self.test_y_file, ]:
            if os.path.exists(file):
                os.remove(file)

    def test_positive_case(self):
        """Позитивный тест: данные корректно разделены."""
        result = make_x_y.make_x_y(self.test_dataset, self.test_x_file, self.test_y_file)
        self.assertTrue(result)

        # Проверяем содержимое файлов
        with open(self.test_x_file, "r") as x_file:
            self.assertEqual(x_file.read().strip(), "2023-10-01\n2023-10-02\n2023-10-03")
        
        with open(self.test_y_file, "r") as y_file:
            self.assertEqual(y_file.read().strip(), "100\n200\n300")

    def test_negative_case_invalid_format(self):
        """Негативный тест: файл с некорректными данными."""
        invalid_dataset = "invalid_dataset.csv"
        with open(invalid_dataset, "w+") as f:
            f.write("2023-10-01;100\ninvalid_line\n2023-10-03;300\n")
        
        result = make_x_y.make_x_y(invalid_dataset, self.test_x_file, self.test_y_file)
        self.assertFalse(result)
        
        # Удаляем временный файл
        os.remove(invalid_dataset)



    def test_exception_handling(self):
        """Тест обработки исключений: отсутствующий файл."""
        non_existent_file = "non_existent.csv"
        with self.assertRaises(FileNotFoundError):
            make_x_y.make_x_y(non_existent_file, self.test_x_file, self.test_y_file)

    def test_empty_file(self):
        """Тест для пустого входного файла."""
        result = make_x_y.make_x_y(self.empty_file, self.test_x_file, self.test_y_file)
        self.assertTrue(result)  # Пустой файл обрабатывается как успешный

        # Проверяем, что созданные файлы также пусты
        with open(self.test_x_file, "r") as x_file:
            self.assertEqual(x_file.read(), "")
        
        with open(self.test_y_file, "r") as y_file:
            self.assertEqual(y_file.read(), "")

class TestSplitByWeek(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения перед каждым тестом."""
        self.test_file = "./test_dataset_week.csv"
        self.result_folder = "./test_results_week"

        # Создаем тестовый CSV-файл
        with open(self.test_file, "w+") as f:
            f.write(
                "2023-10-01;100\n2023-10-02;200\n2023-10-03;300\n"
                "2023-10-08;400\n2023-10-09;500\n2023-10-10;600\n"
            )

        # Удаляем папку результатов, если она существует
        if os.path.exists(self.result_folder):
            for file in os.listdir(self.result_folder):
                os.remove(os.path.join(self.result_folder, file))
            os.rmdir(self.result_folder)

    def tearDown(self):
        """Очистка файлов после тестов."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.result_folder):
            for file in os.listdir(self.result_folder):
                os.remove(os.path.join(self.result_folder, file))
            os.rmdir(self.result_folder)

    def test_positive_case(self):
        """Позитивный тест: функция корректно разделяет данные по неделям."""
        result = split_by_week.split_by_week(self.test_file, self.result_folder)
        self.assertTrue(result)

        # Проверяем, что файлы созданы
        self.assertTrue(os.path.isdir(self.result_folder))
        created_files = os.listdir(self.result_folder)
        self.assertEqual(len(created_files), 3)

        # Проверяем содержимое первого файла
        first_file = os.path.join(self.result_folder, created_files[0])
        with open(first_file, "r") as f:
            content = f.read().strip()
        self.assertEqual(content, "2023-10-01;100\n2023-10-02;200")

    def test_negative_case_invalid_data(self):
        """Негативный тест: некорректные строки в данных."""
        invalid_file = "invalid_dataset.csv"
        with open(invalid_file, "w+") as f:
            f.write("2023-10-01;100\ninvalid_line\n2023-10-03;300\n")

        result = split_by_week.split_by_week(invalid_file, self.result_folder)

        # Удаляем временный файл
        os.remove(invalid_file)
        self.assertFalse(result)

        # Убедимся, что папка результатов не создана
        self.assertFalse(os.path.exists(self.result_folder))



    def test_exception_handling_no_file(self):
        """Тест исключительной ситуации: отсутствующий входной файл."""
        non_existent_file = "non_existent.csv"
        with self.assertRaises(FileNotFoundError):
            split_by_week.split_by_week(non_existent_file, self.result_folder)

    def test_empty_file(self):
        """Тест на пустой файл."""
        empty_file = "empty.csv"
        open(empty_file, "w+").close()

        result = split_by_week.split_by_week(empty_file, self.result_folder)
        
        # Удаляем временный файл
        os.remove(empty_file)

        self.assertTrue(result)  # Пустой файл обрабатывается как успешный

class TestSplitByYear(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения перед каждым тестом."""
        self.test_file = "./test_dataset_year.csv"
        self.result_folder = "./test_results_year"

        # Создаем тестовый CSV-файл
        with open(self.test_file, "w+") as f:
            f.write(
                "2021-01-01;100\n2021-02-01;200\n2022-01-01;300\n"
                "2022-02-01;400\n2023-01-01;500\n"
            )

        # Удаляем папку результатов, если она существует
        if os.path.exists(self.result_folder):
            for file in os.listdir(self.result_folder):
                os.remove(os.path.join(self.result_folder, file))
            os.rmdir(self.result_folder)

    def tearDown(self):
        """Очистка файлов после тестов."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.result_folder):
            for file in os.listdir(self.result_folder):
                os.remove(os.path.join(self.result_folder, file))
            os.rmdir(self.result_folder)

    def test_positive_case(self):
        """Позитивный тест: корректное разделение данных по годам."""
        result = split_by_year.split_by_year(self.test_file, self.result_folder)
        self.assertTrue(result)

        # Проверяем, что файлы созданы
        self.assertTrue(os.path.isdir(self.result_folder))
        created_files = os.listdir(self.result_folder)
        self.assertEqual(len(created_files), 3)

        # Проверяем содержимое файла за 2021 год
        first_file = os.path.join(self.result_folder, created_files[0])
        with open(first_file, "r") as f:
            content = f.read().strip()
        self.assertEqual(content, "2021-01-01;100\n2021-02-01;200")

    def test_negative_case_invalid_data(self):
        """Негативный тест: некорректные строки в данных."""
        invalid_file = "./invalid_dataset.csv"
        with open(invalid_file, "w+") as f:
            f.write("2021-01-01;100\ninvalid_line;invalid_line\n2022-01-01;300\n")

        result = split_by_year.split_by_year(invalid_file, self.result_folder)
        
        # Удаляем временный файл
        os.remove(invalid_file)

        self.assertFalse(result)

        # Убедимся, что папка результатов не создана
        self.assertFalse(os.path.exists(self.result_folder))



    def test_exception_handling_no_file(self):
        """Тест исключительной ситуации: отсутствующий входной файл."""
        non_existent_file = "non_existent.csv"
        with self.assertRaises(FileNotFoundError):
            split_by_year.split_by_year(non_existent_file, self.result_folder)

    def test_empty_file(self):
        """Тест на пустой файл."""
        empty_file = "./empty.csv"
        open(empty_file, "w+").close()

        result = split_by_year.split_by_year(empty_file, self.result_folder)

        # Удаляем временный файл
        os.remove(empty_file)

        self.assertTrue(result)  # Пустой файл обрабатывается как успешный

class TestGetValue(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения перед каждым тестом."""
        self.file1 = "./test_file1.csv"
        self.file2 = "./test_file2.csv"
        
        # Создаем первый тестовый CSV-файл
        with open(self.file1, "w+") as f:
            f.write("date;value\n2023-01-01;100\n2023-01-02;200\n2023-01-03;300\n")
        
        # Создаем второй тестовый CSV-файл
        with open(self.file2, "w+") as f:
            f.write("date;value;\n2023-01-04;400\n2023-01-05;500\n")

    def tearDown(self):
        """Очистка тестового окружения после каждого теста."""
        if os.path.exists(self.file1):
            os.remove(self.file1)
        if os.path.exists(self.file2):
            os.remove(self.file2)

    def test_positive_case(self):
        """Позитивный тест: дата присутствует в файлах."""
        result = find_value.get_value("2023-01-01", [self.file1, self.file2])
        self.assertEqual(result, 100)

        result = find_value.get_value("2023-01-05", [self.file1, self.file2])
        self.assertEqual(result, 500)

    def test_negative_case_date_not_found(self):
        """Негативный тест: дата отсутствует в файлах."""
        result = find_value.get_value("2023-01-10", [self.file1, self.file2])
        self.assertIsNone(result)

    def test_exception_handling_invalid_file(self):
        """Тест исключительной ситуации: файл не существует."""
        with self.assertRaises(FileNotFoundError):
            find_value.get_value("2023-01-01", ["non_existent.csv"])

    def test_combined_datasets(self):
        """Тест работы с объединенными файлами."""
        result = find_value.create_dataset_from_files([self.file1, self.file2])
        self.assertEqual(result.shape[0], 5)  # Объединенный датасет должен содержать 5 строк

        value = find_value.get_value("2023-01-03", [self.file1, self.file2])
        self.assertEqual(value, 300)

class TestAnalysis(unittest.TestCase):
    def setUp(self):
        """Создание тестовых данных для всех тестов"""
        self.df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
            'value': [100, 200, 150, 300]
        })
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        self.df_with_deviation = self.df.copy()
        self.df_with_deviation['deviation_from_mean'] = [50, 150, 100, 250]

    def test_calculate_mean_by_month_positive(self):
        """Позитивный тест для функции calculate_mean_by_month"""
        result = data_analysis.calculate_mean_by_month(self.df)
        self.assertEqual(len(result), 1)  # Только один месяц
        self.assertAlmostEqual(result['value'].iloc[0], 187.5, places=1)

    def test_filter_by_deviation_positive(self):
        """Позитивный тест для функции filter_by_deviation"""
        threshold = 100
        filtered_df = data_analysis.filter_by_deviation(self.df_with_deviation, threshold)
        self.assertEqual(len(filtered_df), 3)  # Ожидаем 2 строки
        self.assertTrue((filtered_df['deviation_from_mean'] >= threshold).all())

    def test_filter_by_date_positive(self):
        """Позитивный тест для функции filter_by_date"""
        start_date = '2023-01-02'
        end_date = '2023-01-03'
        filtered_df = data_analysis.filter_by_date(self.df, start_date, end_date)
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue((filtered_df['date'] >= pd.to_datetime(start_date)).all())
        self.assertTrue((filtered_df['date'] <= pd.to_datetime(end_date)).all())

    def test_filter_by_deviation_negative(self):
        """Негативный тест для функции filter_by_deviation"""
        with self.assertRaises(ValueError):
            data_analysis.filter_by_deviation(self.df, 100)  # Нет столбца 'deviation_from_mean'

    def test_filter_by_date_negative(self):
        """Негативный тест для функции filter_by_date"""
        filtered_df = data_analysis.filter_by_date(self.df, '2024-01-01', '2024-01-31')  # Даты не попадают
        self.assertEqual(len(filtered_df), 0)

    def test_filter_by_date_exception(self):
        """Исключительная ситуация: некорректный формат даты"""
        with self.assertRaises(Exception):
            data_analysis.filter_by_date(self.df, 'invalid-date', '2023-01-03')


if __name__ == '__main__':
    unittest.main()

