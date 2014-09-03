from PySide.QtGui import QStandardItemModel, QStandardItem, QListView, QApplication
import sys


def is_clicked(index):
    # trying to access the item via internalPointer
    print(index.internalPointer().text())


app = QApplication(sys.argv)
model = QStandardItemModel()
item = QStandardItem()
item.setText("Test")
model.appendRow(item)
view = QListView()
view.setMinimumSize(200, 200)

view.setModel(model)
view.clicked.connect(is_clicked)
#this works fine
view.clicked.emit(model.createIndex(0, 0, item))
# now click the Test entry manually, the program will crash

view.show()
app.exec_()