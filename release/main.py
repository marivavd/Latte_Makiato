import sys
import sqlite3
from release.UI import main1, add_edit
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton


class Example(QMainWindow, main1.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Git и желтые окружности')
        con = sqlite3.connect("release/data/coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT name FROM coffee""").fetchall()
        for elem in result:
            self.comboBox.addItem(*elem)
        con.close()
        self.do_paint = False
        self.first = False
        self.pushButton.clicked.connect(self.find)
        self.pushButton_2.clicked.connect(self.add)
        self.pushButton_3.clicked.connect(self.change)

    def add(self):
        self.new = Change_Add('Добавить', 'add')
        self.new.show()
        self.close()

    def change(self):
        self.new = Change_Add('Изменить', self.comboBox.currentText())
        self.new.show()
        self.close()

    def find(self):
        name = self.comboBox.currentText()
        con = sqlite3.connect('release/data/coffee.sqlite')
        cur = con.cursor()
        text = self.lineEdit.text()
        result = cur.execute(f"""SELECT * FROM coffee
                                        WHERE name like '{name}'""").fetchall()
        self.lineEdit.setText(str(result[0][0]))
        self.lineEdit_2.setText(str(result[0][2]))
        self.lineEdit_3.setText(str(result[0][3]))
        self.lineEdit_4.setText(str(result[0][4]))
        self.lineEdit_5.setText(str(result[0][5]))
        self.lineEdit_6.setText(str(result[0][6]))
        self.lineEdit_7.setText(str(result[0][7]))
        con.close()

class Change_Add(QMainWindow, add_edit.Ui_MainWindow):
    def __init__(self, name, text):
        super().__init__()
        self.setupUi(self)
        self.button_2 = QPushButton(self)
        self.button_2.setText('‹-')
        self.button_2.move(2, 2)
        self.button_2.setMaximumSize(60, 60)
        self.button_2.setFont(QFont('Arial', 20))
        self.button_2.clicked.connect(self.back)
        self.pushButton.setText(name)
        self.pushButton.clicked.connect(self.run)
        self.text = text
        if text == 'add':
            con = sqlite3.connect('release/data/coffee.sqlite')
            cur = con.cursor()
            result = cur.execute(f"""SELECT COUNT(*) FROM coffee""").fetchall()
            self.lineEdit.setText(str(result[0][0] + 1))
            con.close()
        else:
            con = sqlite3.connect('release/data/coffee.sqlite')
            cur = con.cursor()
            result = cur.execute(f"""SELECT * FROM coffee
                                                    WHERE name like '{text}'""").fetchall()
            self.lineEdit.setText(str(result[0][0]))
            self.lineEdit_2.setText(str(result[0][1]))
            self.lineEdit_3.setText(str(result[0][2]))
            self.lineEdit_4.setText(str(result[0][3]))
            self.lineEdit_5.setText(str(result[0][4]))
            self.lineEdit_6.setText(str(result[0][5]))
            self.lineEdit_7.setText(str(result[0][6]))
            self.lineEdit_8.setText(str(result[0][7]))
            con.close()

    def back(self):
        self.new = Example()
        self.new.show()
        self.close()

    def run(self):
        if self.pushButton.text() == 'Изменить':
            con = sqlite3.connect('release/data/coffee.sqlite')
            cur = con.cursor()
            cur.execute(f"""UPDATE coffee SET ID = {self.lineEdit.text()}, name = '{self.lineEdit_2.text()}',
            sort_name = '{self.lineEdit_3.text()}', step_obj = '{self.lineEdit_4.text()}', 'mol/zern' = '{self.lineEdit_5.text()}',
            taste = '{self.lineEdit_6.text()}', price = {self.lineEdit_7.text()}, volume = {self.lineEdit_8.text()}
            WHERE name like '{self.text}'""").fetchall()
            con.commit()
        else:
            con = sqlite3.connect('release/data/coffee.sqlite')
            cur = con.cursor()
            cur.execute(f"""INSERT INTO coffee VALUES ({self.lineEdit.text()}, '{self.lineEdit_2.text()}',
                        '{self.lineEdit_3.text()}', '{self.lineEdit_4.text()}', '{self.lineEdit_5.text()}',
                        '{self.lineEdit_6.text()}', {self.lineEdit_7.text()}, {self.lineEdit_8.text()})""").fetchall()
            con.commit()
        con.close()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Example()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
