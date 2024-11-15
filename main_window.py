import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, \
QPushButton, QHBoxLayout, QMessageBox, QMenuBar, QAction, QMainWindow, QFileDialog, QCalendarWidget, \
QDialog
from PyQt5.QtGui import QIcon


from util import make_x_y, find_value, split_by_week, split_by_year, create_annotation

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

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Дата", "Стоимость"])

        layout.addWidget(self.table)

        button_layout = QHBoxLayout()

        self.buttonFindValue = QPushButton('Получить данные')
        self.buttonXY = QPushButton('Разделить на x и y')
        self.buttonYearsSplit = QPushButton('Разделить по годам')
        self.buttonWeeksSplit = QPushButton('Разделить по неделям')

        self.buttonFindValue.setEnabled(False)
        self.buttonXY.setEnabled(False)
        self.buttonYearsSplit.setEnabled(False)
        self.buttonWeeksSplit.setEnabled(False)

        button_layout.addWidget(self.buttonFindValue)
        button_layout.addWidget(self.buttonXY)
        button_layout.addWidget(self.buttonYearsSplit)
        button_layout.addWidget(self.buttonWeeksSplit)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.setWindowTitle('Крутейшее приложение')
        self.setGeometry(400, 400, 400, 400)
        self.show()

        self.buttonFindValue.clicked.connect(self.find_value)
        self.buttonXY.clicked.connect(self.split_x_y)
        self.buttonYearsSplit.clicked.connect(self.split_by_years)
        self.buttonWeeksSplit.clicked.connect(self.split_by_weeks)

    def on_file_open_click(self):
        self.datasetpaths = QFileDialog.getOpenFileNames(self, 'Выберите файл',filter="*.csv")[0]
        if len(self.datasetpaths) == 0:
            return
        self.buttonFindValue.setEnabled(True)
        self.buttonXY.setEnabled(True)
        self.buttonYearsSplit.setEnabled(True)
        self.buttonWeeksSplit.setEnabled(True)
        i = 0
        for index, line in find_value.DataFrameIterator(find_value.create_dataset_from_files(self.datasetpaths)):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(line.iloc[0])))
            self.table.setItem(i, 1, QTableWidgetItem(str(line.iloc[1])))
            i+=1
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
        selected_date = self.open_calendar()
        if selected_date != None:
            result = find_value.get_value(selected_date, self.datasetpaths)
            if result != None:
                QMessageBox.information(self, "Значение найдено", f"Значение {selected_date} было равно {result}")
            else:
                QMessageBox.information(self, "Значение не найдено!", "Значения за эту дату нет!")
        else:
            QMessageBox.warning(self, "Ошибка", "Дата не была выбрана")
        

    def open_calendar(self):
        dialog = QDialog(self)
        dialog.setWindowTitle('Выбор даты')
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
