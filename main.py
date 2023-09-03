from PyQt5.QtWidgets import QMainWindow,QHeaderView, QApplication, QMessageBox,  QTableWidget, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys
from database import Sql
Ui_MainWindow, _ = uic.loadUiType("tasks.ui")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sql = Sql()
        self.refresh()
        self.handel_btns()

    def handel_btns(self):
        self.comboBox.currentIndexChanged.connect(self.getText)
        self.search_btn.clicked.connect(self.search)
        self.refresh_btn.clicked.connect(self.refresh)
        self.submit_btn.clicked.connect(self.submit)
        self.delete_btn.clicked.connect(self.deleteBtn)
        self.update_btn.clicked.connect(self.update_status)
    
    def update_status(self):
        id = self.update_spin.value()
        status = self.status_combo_update.currentText()
        reply = QMessageBox.question(self, "Confirmation", f"Are you sure you want to update the row with id = {id}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sql.update(id, status)
        else:
            pass
        
    def deleteBtn(self):
        id=self.spinBox.value()
        reply = QMessageBox.question(self, "Confirmation", f"Are you sure you want to delete the row with id = {id}?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.sql.delete(int(id))
        else:
            pass

    def submit(self):
        date = self.dateEdit.date().toPyDate()
        status = self.status_combo.currentText()
        task = self.ptxt.toPlainText()
        self.ptxt.clear()
        if task:
            self.sql.insert(task, status, date)
            messageBox = QMessageBox()
            messageBox.setText("Successfuly Submited.")
            messageBox.setStandardButtons(QMessageBox.Ok)
            messageBox.exec() 
        else:
            pass

    def refresh(self):
        result = self.sql.get_all_data()
        self.loadTab(result)

    def search(self):
        column = self.getText()
        text = self.lineEdit.text()
        result = self.sql.search(column, text)
        self.loadTab(result)

    def getText(self):
        text = self.comboBox.currentText()
        return text

    def loadTab(self, result):   
        self.table.setRowCount(0)
        for row_nbr , row_data in enumerate(result):
            self.table.insertRow(row_nbr)
            for col_nbr, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_nbr, col_nbr, item)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, 100)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
