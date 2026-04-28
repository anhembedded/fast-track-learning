Qt có 3 abstract model chính:

1. List model
	QAbstractListModel
2. Table model
	QAbstractTableModel
3. Tree model
	QAbstractItemModel

## Core concepts của mọi model
Dù list/table/tree, luôn có 3 thứ:
## 1. rowCount()
Có bao nhiêu hàng.
## 2. columnCount()
(table/tree có)
Có bao nhiêu cột.
## 3. data()
Trả dữ liệu.

```Python
from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt
from PySide6.QtWidgets import QApplication, QListView
import sys

class NameModel(QAbstractListModel):
    def __init__(self, names):
        super().__init__()
        self.names = names
    def rowCount(self, parent):
        return len(self.names)
    def data(self, index : QModelIndex, role):
        if role == Qt.DisplayRole:
            return self.names[index.row()]

names = ["Apple", "Banana", "Orange"]
app = QApplication(sys.argv)
model = NameModel(["Apple", "Banana", "Orange"])

view = QListView()
view.setModel(model)   # Gắn model vào view
view.show()

sys.exit(app.exec())
```


|Role|Value|Description|
|---|---|---|
|`Qt.DisplayRole`|`0`|The key data to be rendered in the form of text. ([QString](https://doc.qt.io/qt-5/qstring.html))|
|`Qt.DecorationRole`|`1`|The data to be rendered as a decoration in the form of an icon. ([QColor](https://doc.qt.io/qt-5/qcolor.html), [QIcon](https://doc.qt.io/qt-5/qicon.html) or [QPixmap](https://doc.qt.io/qt-5/qpixmap.html))|
|`Qt.EditRole`|`2`|The data in a form suitable for editing in an editor. ([QString](https://doc.qt.io/qt-5/qstring.html))|
|`Qt.ToolTipRole`|`3`|The data displayed in the item's tooltip. ([QString](https://doc.qt.io/qt-5/qstring.html))|
|`Qt.StatusTipRole`|`4`|The data displayed in the status bar. ([QString](https://doc.qt.io/qt-5/qstring.html))|
|`Qt.WhatsThisRole`|`5`|The data displayed for the item in "What's This?" mode. ([QString](https://doc.qt.io/qt-5/qstring.html))|
|`Qt.SizeHintRole`|`13`|The size hint for the item that will be supplied to views. ([QSize](https://doc.qt.io/qt-5/qsize.html))|
