import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
QPushButton, QHBoxLayout, QMessageBox, QMenuBar, QAction, QMainWindow, QFileDialog, QCalendarWidget, \
QDialog, QTabWidget, QSpinBox
from PyQt5.QtGui import QIcon


from util import make_x_y, find_value, split_by_week, split_by_year, create_annotation, data_analysis

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('./baka.png'))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        self.file_action_open = QAction('Открыть', self)
        self.file_action_open.triggered.connect(self.on_file_open_click)
        self.file_action_annotation = QAction('Создать аннотацию', self)
        self.file_action_annotation.setEnabled(False)
        self.file_action_annotation.triggered.connect(self.on_annotation_click)

        file_menu.addAction(self.file_action_open)
        file_menu.addAction(self.file_action_annotation)

        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Первая вкладка
        self.splitting_tab = QWidget()
        splitting_layout = QVBoxLayout(self.splitting_tab)

        self.tab_widget.addTab(self.splitting_tab, "Разделение")

        self.split_table = QTableWidget()
        self.split_table.setColumnCount(2)
        self.split_table.setHorizontalHeaderLabels(["Дата", "Стоимость"])

        splitting_layout.addWidget(self.split_table)

        split_button_layout = QHBoxLayout()

        self.buttonFindValue = QPushButton('Получить данные')
        self.buttonXY = QPushButton('Разделить на x и y')
        self.buttonYearsSplit = QPushButton('Разделить по годам')
        self.buttonWeeksSplit = QPushButton('Разделить по неделям')

        self.buttonFindValue.setEnabled(False)
        self.buttonXY.setEnabled(False)
        self.buttonYearsSplit.setEnabled(False)
        self.buttonWeeksSplit.setEnabled(False)

        split_button_layout.addWidget(self.buttonFindValue)
        split_button_layout.addWidget(self.buttonXY)
        split_button_layout.addWidget(self.buttonYearsSplit)
        split_button_layout.addWidget(self.buttonWeeksSplit)

        splitting_layout.addLayout(split_button_layout)

        self.setWindowTitle('Крутейшее приложение')
        self.setGeometry(400, 400, 400, 400)
        self.show()

        self.buttonFindValue.clicked.connect(self.find_value)
        self.buttonXY.clicked.connect(self.split_x_y)
        self.buttonYearsSplit.clicked.connect(self.split_by_years)
        self.buttonWeeksSplit.clicked.connect(self.split_by_weeks)

        # Вторая вкладка
        self.processing_tab = QWidget()
        processing_layout = QVBoxLayout(self.processing_tab)
        
        self.tab_widget.addTab(self.processing_tab, "Обработка")

        self.proc_table = QTableWidget()
        self.proc_table.setColumnCount(4)
        self.proc_table.setHorizontalHeaderLabels(["Дата", "Стоимость", "Отклонение от медианы", "Отклонение от среднего"])

        processing_layout.addWidget(self.proc_table)

        proc_button_layout = QHBoxLayout()
        self.button_deviation = QPushButton('Фильтр по отклонению')
        self.button_date = QPushButton('Фильтр по дате')
        self.button_whole = QPushButton('Сделать график за весь период')
        self.button_month = QPushButton('Сделать график за месяц')

        self.button_deviation.clicked.connect(self.filter_deviation)
        self.button_date.clicked.connect(self.filter_date)
        self.button_whole.clicked.connect(self.graph_whole_period)
        self.button_month.clicked.connect(self.graph_month)

        proc_button_layout.addWidget(self.button_deviation)
        proc_button_layout.addWidget(self.button_date)
        proc_button_layout.addWidget(self.button_whole)
        proc_button_layout.addWidget(self.button_month)

        self.button_deviation.setEnabled(False)
        self.button_date.setEnabled(False)
        self.button_whole.setEnabled(False)
        self.button_month.setEnabled(False)

        processing_layout.addLayout(proc_button_layout)
        
        # Третья вкладка
        self.info_tab = QWidget()
        info_layout = QVBoxLayout(self.info_tab)
        
        self.tab_widget.addTab(self.info_tab, "Информация")

        self.info_table = QTableWidget()
        self.info_table.setColumnCount(4)
        self.info_table.setHorizontalHeaderLabels(["Характеристика", "Стоимость", "Отклонение от медианы", "Отклонение от среднего"])

        info_layout.addWidget(self.info_table)

        info_button_layout = QHBoxLayout()
        self.button_info = QPushButton('Вывести информацию')

        self.button_info.clicked.connect(self.get_info)

        info_button_layout.addWidget(self.button_info)

        self.button_info.setEnabled(False)

        info_layout.addLayout(info_button_layout)

    def on_file_open_click(self):
        self.datasetpaths = QFileDialog.getOpenFileNames(self, 'Выберите файл',filter="*.csv")[0]
        if len(self.datasetpaths) == 0:
            return
        self.buttonFindValue.setEnabled(True)
        self.buttonXY.setEnabled(True)
        self.buttonYearsSplit.setEnabled(True)
        self.buttonWeeksSplit.setEnabled(True)

        self.button_deviation.setEnabled(True)
        self.button_date.setEnabled(True)
        self.button_whole.setEnabled(True)
        self.button_month.setEnabled(True)
        self.df = data_analysis.prepare_df(find_value.create_dataset_from_files(self.datasetpaths))
        
        self.button_info.setEnabled(True)

        self.fill_table(self.df, self.split_table)
        self.fill_table(self.df, self.proc_table)
        self.file_action_annotation.setEnabled(True)

    def on_annotation_click(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для файла аннотации')
        if result_folder == "":
            QMessageBox.information(self, "Ошибка!", "Вы не выбрали папку")
            return
        if create_annotation.create_annotation(filename=self.datasetpaths[0], result_folder=result_folder):
            QMessageBox.information(self, "Успех", "Файл создан")
        else:
            QMessageBox.information(self, "Ошибка!", "Что-то пошло не так!")
        
    
    def find_value(self):
        selected_date = self.open_calendar('Введите дату')
        if selected_date != None:
            result = find_value.get_value(selected_date, self.datasetpaths)
            if result != None:
                QMessageBox.information(self, "Значение найдено", f"Значение {selected_date} было равно {result}")
            else:
                QMessageBox.information(self, "Значение не найдено!", "Значения за эту дату нет!")
        else:
            QMessageBox.warning(self, "Ошибка", "Дата не была выбрана")
        

    def open_calendar(self, title):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setGeometry(300, 300, 300, 250)

        layout = QVBoxLayout(dialog)

        calendar = QCalendarWidget(dialog)
        layout.addWidget(calendar)

        btn_select = QPushButton('Выбрать дату', dialog)
        layout.addWidget(btn_select)

        selected_date = None

        def select_date():
            nonlocal selected_date
            selected_qdate = calendar.selectedDate()
            selected_date = selected_qdate.toString("yyyy-MM-dd")
            dialog.accept()

        btn_select.clicked.connect(select_date)

        if dialog.exec_() == QDialog.Accepted:
            return selected_date  

        return None 
    
    def split_x_y(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для выходных файлов')
        if result_folder == "":
            QMessageBox.information(self, "Ошибка!", "Вы не выбрали папку")
            return
        if make_x_y.make_x_y(filename=self.datasetpaths[0],x_file=result_folder+"/x.csv", y_file=result_folder+"/y.csv"):
            QMessageBox.information(self, "Успех", "Файлы созданы")
        else:
            QMessageBox.information(self, "Ошибка!", "Что-то пошло не так!")
        
    def split_by_years(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для выходных файлов')
        if result_folder == "":
            QMessageBox.information(self, "Ошибка!", "Вы не выбрали папку")
            return
        if split_by_year.split_by_year(filename=self.datasetpaths[0],result_folder=result_folder):
            QMessageBox.information(self, "Успех", "Файлы созданы")
        else:
            QMessageBox.information(self, "Ошибка!", "Что-то пошло не так!")
    def split_by_weeks(self):
        result_folder = QFileDialog.getExistingDirectory(self, caption='Выберите папку для выходных файлов')
        if result_folder == "":
            QMessageBox.information(self, "Ошибка!", "Вы не выбрали папку")
            return
        if split_by_week.split_by_week(filename=self.datasetpaths[0],result_folder=result_folder):
            QMessageBox.information(self, "Успех", "Файлы созданы")
        else:
            QMessageBox.information(self, "Ошибка!", "Что-то пошло не так!")

    def filter_deviation(self):
        selected_threshold = self.open_deviation_dialog()
        print(selected_threshold)
        if selected_threshold != None:
            result = pd.DataFrame()
            try:
                result = data_analysis.filter_by_deviation(self.df, selected_threshold)
            except:
                QMessageBox.information(self, "Ошибка!", "Отфильтровать не получилось!")
            self.fill_table(result, self.proc_table)
        else:
            QMessageBox.warning(self, "Ошибка", "Отклонение не было выбрано")
        

    def open_deviation_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Введите отклонение')
        dialog.setGeometry(300, 300, 300, 250)

        layout = QVBoxLayout(dialog)

        spinBox = QSpinBox()
        layout.addWidget(spinBox)

        btn_select = QPushButton('Подтвердить', dialog)
        layout.addWidget(btn_select)

        selected_threshold = None

        def input_threshold():
            nonlocal selected_threshold
            selected_threshold = spinBox.value()
            dialog.accept()

        btn_select.clicked.connect(input_threshold)

        if dialog.exec_() == QDialog.Accepted:
            return selected_threshold  

        return None 
    
    def fill_table(self, df: pd.DataFrame, table : QTableWidget):
        table.setRowCount(0)
        i = 0
        for index, line in find_value.DataFrameIterator(df):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem(str(line.iloc[0])))
            table.setItem(i, 1, QTableWidgetItem(str(line.iloc[1])))
            table.setItem(i, 2, QTableWidgetItem(str(line.iloc[2])))
            table.setItem(i, 3, QTableWidgetItem(str(line.iloc[3])))

            i+=1

    def filter_date(self):
        start_date = self.open_calendar('Введите начальную дату')
        end_date = self.open_calendar('Введите конечную дату')
        if start_date != None and end_date != None:
            result = pd.DataFrame()
            try:
                result = data_analysis.filter_by_date(df=self.df, start_date=start_date, end_date=end_date)
            except:
                QMessageBox.information(self, "Ошибка!", "Отфильтровать не получилось!")
            self.fill_table(result, self.proc_table)
        else:
            QMessageBox.warning(self, "Ошибка", "Период не был выбран")
    
    def graph_whole_period(self):
        data_analysis.create_graph_whole_period(self.df)

    def graph_month(self):
        month = self.open_calendar('Введите месяц')
        if month != None:
            data_analysis.create_graph_month(self.df, month[:-3])
            
    def get_info(self):
        median_value = self.df['value'].median()
        mean_value = self.df['value'].mean()

        stats = self.df[['value', 'deviation_from_median', 'deviation_from_mean']].describe()
        stats.insert(loc=0, column='index', value=stats.index)
        row = ['median',median_value,0,mean_value-median_value]
        stats.loc[len(stats.index)] = row
        self.fill_table(stats, self.info_table)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
