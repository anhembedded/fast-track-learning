```Python
class ListViewModel(QAbstractListModel):
    def __init__(self, names):
        super().__init__()
        self.names = names

    def rowCount(self, parent):
        return len(self.names)

    def data(self, index: QModelIndex, role):
        if role == Qt.DisplayRole:
            return self.names[index.row()]

    def addList(self, name : str):
        self.beginInsertRows(QModelIndex(), self.rowCount(None), self.rowCount(None))
        self.names.append(name)
        self.endInsertRows()
```

API:
