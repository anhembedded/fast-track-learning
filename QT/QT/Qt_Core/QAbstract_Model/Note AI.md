Hay, giờ đi đúng đường rồi đó.

Nếu hiểu **QAbstract*Model** theo hướng “interface cho data adapters” thì cả Qt Model/View bỗng dễ hiểu hơn nhiều.

# Bức tranh lớn trước

Qt có 3 abstract model chính:

### 1. List model

```text
QAbstractListModel
```

Dữ liệu 1 chiều:

```text
Task1
Task2
Task3
```

Giống:

- Python list
    

```python
["a","b","c"]
```

- C array
    

```c
arr[3]
```

Dùng với:

- `QListView`
    
- `QComboBox`
    

---

---

## 2. Table model

```text
QAbstractTableModel
```

2 chiều:

```text
Name   Age

Tom    25
Anna   30
```

Giống:

```python
[
 ["Tom",25],
 ["Anna",30]
]
```

Dùng:

- `QTableView`
    

Giống spreadsheet.

---

## 3. Tree model

```text
QAbstractItemModel
```

Đây là cha lớn nhất.

Dùng cho:

```text
Root

 ├── Folder1

 │     ├ file1

 │     └ file2

 └── Folder2
```

Giống:

- file system
    
- JSON tree
    
- XML DOM
    

Dùng:

- `QTreeView`
    

---

# Relationship

```text
QAbstractItemModel

   |

   +---QAbstractListModel

   |

   +---QAbstractTableModel
```

Inheritance.

---

# Nếu là software engineer

Hãy nghĩ:

```text
QAbstractItemModel

là generic interface

QAbstractListModel

là specialization
```

giống:

```cpp
class Container

class Vector : Container

class Map : Container
```

---

# Core concepts của mọi model

Dù list/table/tree, luôn có 3 thứ:

## 1. rowCount()

Có bao nhiêu hàng.

---

## 2. columnCount()

(table/tree có)

Có bao nhiêu cột.

---

## 3. data()

Trả dữ liệu.

---

---

# Thực hành 1 — QAbstractListModel

Viết model cho danh sách tên.

```python
from PySide6.QtCore import *

class NameModel(QAbstractListModel):

    def __init__(self,names):

        super().__init__()

        self.names=names


    def rowCount(self,parent):

        return len(self.names)


    def data(self,index,role):

        if role==Qt.DisplayRole:

            return self.names[index.row()]
```

---

## Bài tập 1

Làm:

```text
Apple

Banana

Orange
```

show ra `QListView`

---

---

# Thực hành 2 — thêm item runtime

Thêm:

```python
beginInsertRows()

endInsertRows()
```

```python
def add_item(self,name):

    self.beginInsertRows(
        QModelIndex(),
        self.rowCount(None),
        self.rowCount(None)
    )

    self.names.append(name)

    self.endInsertRows()
```

---

## Bài tập 2

Viết nút:

```text
Add Task
```

bấm thêm row mới.

---

---

# Thực hành 3 — Table model

```python
class PersonModel(QAbstractTableModel):

    def __init__(self,data):

        super().__init__()

        self.people=data


    def rowCount(self,parent):

        return len(self.people)


    def columnCount(self,parent):

        return 2


    def data(self,index,role):

        if role==Qt.DisplayRole:

            row=index.row()

            col=index.column()

            return self.people[row][col]
```

---

## Bài tập 3

Hiện:

```text
Name  Age

Tom   20

Ann   30
```

trên `QTableView`

---

# Bước quan trọng: Roles

Hồi nãy chỉ dùng:

```python
Qt.DisplayRole
```

Nhưng còn:

- Checkboxes
    

```python
Qt.CheckStateRole
```

- màu
    

```python
Qt.ForegroundRole
```

- font
    

```python
Qt.FontRole
```

---

## Bài tập 4

Todo done:

```text
☑ Learn Qt

☐ Learn Python
```

dùng `CheckStateRole`

---

---

# Bước quan trọng: Editing

Để sửa dữ liệu:

phải thêm:

```python
setData()

flags()
```

---

## Bài tập 5

Cho user sửa cell Age.

---

---

# Học Tree (khó nhất)

Cái này để sau.

Vì phải hiểu:

- QModelIndex
    
- parent()
    
- children()
    

rồi mới học.

---

# Roadmap tôi khuyên

Thứ tự này đúng:

```text
1 QAbstractListModel

2 beginInsertRows

3 setData

4 Roles

5 QAbstractTableModel

6 Proxy models

7 QAbstractItemModel (tree)
```

Đừng nhảy tree sớm.

95% người học chết ở đó.

---

# Proxy model (siêu hay)

Sau này bạn sẽ thấy:

```text
Source model
   ↓

SortFilterProxyModel

   ↓

View
```

Giống middleware.

Cực đẹp.

---

# Nhìn dưới góc design patterns

Qt Model/View dính:

- Adapter  
    Adapter Pattern
    
- Observer  
    Observer Pattern
    
- MVC  
    Model–View–Controller
    
- Proxy  
    Proxy Pattern
    

Nó là một đống pattern ghép lại.

---

# Mini curriculum cho bạn

Tôi sẽ giao bài như học thật:

## Level 1

Viết:

- String list model
    
- Add/remove item
    

---

## Level 2

Viết:

Todo app:

```text
[x] Learn Qt

[ ] Learn Python
```

---

## Level 3

Viết:

Task table

```text
Task   Priority   Done
```

---

## Level 4

Viết:

File explorer tree model.

---

Đến level 4 là hiểu Qt model/view thật.

---

## Một insight rất quan trọng

**QAbstractModel không phải data structure.**

Nó là:

```text
Protocol for exposing data
```

Câu này nhớ kỹ.

Cực quan trọng.

---

Nếu muốn, tôi có thể dạy tiếp **QModelIndex** (cái khó nhất và hay nhất) như kiểu con trỏ/handle của kernel. Đó là chỗ nhiều C++/embedded dev thấy “à, ra là vậy”.