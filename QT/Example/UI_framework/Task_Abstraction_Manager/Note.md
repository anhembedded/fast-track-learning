Chúng ta sẽ đi sâu vào **Cấp độ 3: Task Abstraction & Manager**. Đây là bước nhảy quan trọng từ việc chỉ chạy thread thô sang một kiến trúc có tổ chức, dễ bảo trì và mở rộng. Mình sẽ giảng từ khái niệm đến chi tiết từng thành phần, kèm sơ đồ UML để bạn hình dung rõ ràng.

---

## 🧠 Vì sao cần Task Abstraction & Manager?

Khi bạn có nhiều loại tác vụ (tải file, xử lý ảnh, truy vấn DB...), mỗi loại đều có chung nhu cầu:

- Báo tiến độ (progress).
- Gửi thông báo/log.
- Cho phép **hủy bỏ** (cancel).
- Có trạng thái rõ ràng (đang chờ, đang chạy, hoàn thành, lỗi...).

Thay vì lặp code cho từng loại, ta **trừu tượng hóa** (abstraction) thành một `BaseTask` chứa mọi hành vi chung. Một `TaskManager` sẽ chịu trách nhiệm quản lý vòng đời của tất cả task, phân phối vào thread pool.

**Lợi ích**:
- Viết một lần, dùng cho mọi loại task.
- Dễ thêm tính năng mới (pause/resume, ưu tiên).
- Tập trung xử lý signal, tránh lỗi thread-safety.
- Tách biệt logic công việc với giao diện (Mediator).

---

## 🧱 Phân tích từng thành phần

### 1. `TaskStatus` – enum trạng thái
```python
from enum import Enum
class TaskStatus(Enum):
    PENDING = 0
    RUNNING = 1
    COMPLETED = 2
    CANCELLED = 3
    FAILED = 4
```
Giúp UI biết task đang ở đâu để hiển thị phù hợp.

### 2. `TaskSignals` – cầu nối tín hiệu (QObject)
```python
from PySide6.QtCore import QObject, Signal
class TaskSignals(QObject):
    progress = Signal(int)        # phần trăm 0-100
    message = Signal(str)         # log
    finished = Signal()           # hoàn tất (dù thành công, lỗi, hủy)
    error = Signal(str)           # thông báo lỗi
```
Mỗi `BaseTask` sở hữu một instance `TaskSignals`. Vì `QRunnable` không có signal, ta dùng QObject bên trong để phát sự kiện về main thread an toàn.

> **Tại sao không dùng `QMetaObject.invokeMethod` như Cấp độ 2?**  
> Ở đây ta vẫn dùng `TaskSignals` như một bridge nhưng gắn liền với task, giúp kết nối trong Manager linh hoạt hơn.

### 3. `BaseTask` – lớp trừu tượng (QRunnable)
```python
from PySide6.QtCore import QMutex, QMutexLocker
import uuid

class BaseTask(QRunnable):
    def __init__(self):
        super().__init__()
        self.id = str(uuid.uuid4())[:8]
        self.status = TaskStatus.PENDING
        self.signals = TaskSignals()
        self._is_cancelled = False
        self._mutex = QMutex()

    def cancel(self):
        with QMutexLocker(self._mutex):
            self._is_cancelled = True

    def is_cancelled(self):
        with QMutexLocker(self._mutex):
            return self._is_cancelled

    def run(self):
        self.status = TaskStatus.RUNNING
        try:
            self._execute()   # phần việc cụ thể
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.signals.error.emit(str(e))
        else:
            self.status = TaskStatus.COMPLETED
        finally:
            self.signals.finished.emit()

    def _execute(self):
        raise NotImplementedError("Subclass must implement _execute")
```

**Phân tích quan trọng**:
- `run()` là entry-point của QRunnable. Nó gọi `_execute()`.
- Có cơ chế hủy an toàn với `QMutex`: vì task chạy ở thread khác, việc đọc/ghi cờ huỷ cần được bảo vệ.
- Luôn emit `finished` dù kết thúc kiểu gì → Manager có thể dọn dẹp.

### 4. Task cụ thể (ví dụ)
```python
class DownloadTask(BaseTask):
    def __init__(self, url, dest):
        super().__init__()
        self.url = url
        self.dest = dest

    def _execute(self):
        # giả lập tải file
        for i in range(1, 101):
            if self.is_cancelled():
                self.signals.message.emit("Download cancelled")
                return  # dừng sớm, run() sẽ vẫn emit finished
            time.sleep(0.05)
            self.signals.progress.emit(i)
            self.signals.message.emit(f"Downloading... {i}%")
```

### 5. `TaskManager` – trung tâm điều phối
```python
class TaskManager(QObject):
    task_added = Signal(BaseTask)
    task_removed = Signal(str)  # truyền task_id

    def __init__(self, max_concurrent=4):
        super().__init__()
        self.pool = QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(max_concurrent)
        self._tasks = {}  # task_id -> BaseTask

    def submit(self, task: BaseTask):
        self._tasks[task.id] = task
        # Dọn dẹp khi task kết thúc
        task.signals.finished.connect(lambda tid=task.id: self._on_finished(tid))
        self.task_added.emit(task)
        self.pool.start(task)

    def cancel(self, task_id: str):
        task = self._tasks.get(task_id)
        if task:
            task.cancel()

    def _on_finished(self, task_id):
        if task_id in self._tasks:
            del self._tasks[task_id]
            self.task_removed.emit(task_id)
```

---

## 🔄 Tương tác giữa các thành phần (sequence)

Khi người dùng nhấn "Tải file", UI gọi `TaskManager.submit(download_task)`:

1. TaskManager lưu task vào `_tasks`, kết nối `task.signals.finished` → dọn dẹp.
2. TaskManager emit `task_added`.
3. Gọi `pool.start(task)` → `task.run()` được chạy trong thread pool.
4. Trong `_execute()`:
   - Task kiểm tra `is_cancelled()` định kỳ.
   - Emit `progress`, `message` qua `task.signals`.
5. Kết thúc (hoặc lỗi, hủy): `signals.finished` phát ra.
6. `TaskManager._on_finished` xóa task khỏi danh sách, emit `task_removed`.
7. UI (qua Mediator) nhận các signal để cập nhật.

---

## 📊 Sơ đồ UML (PlantUML)

### 🧩 Class Diagram

```
@startuml
skinparam classAttributeIconSize 0

class TaskStatus <<enumeration>> {
    PENDING
    RUNNING
    COMPLETED
    CANCELLED
    FAILED
}

class TaskSignals <<QObject>> {
    + progress(int)
    + message(str)
    + finished()
    + error(str)
}

class BaseTask <<QRunnable, abstract>> {
    - id : str
    - status : TaskStatus
    - signals : TaskSignals
    - _is_cancelled : bool
    - _mutex : QMutex
    + __init__()
    + cancel()
    + is_cancelled() : bool
    + run()
    {abstract} _execute()
}

class DownloadTask {
    - url : str
    - dest : str
    + _execute()
}

class TaskManager <<QObject>> {
    - pool : QThreadPool
    - _tasks : dict
    + submit(task : BaseTask)
    + cancel(task_id : str)
    - _on_finished(task_id)
    signal task_added(BaseTask)
    signal task_removed(str)
}

class UIMediator <<QObject>> {
    + connectSignals()
}

BaseTask "1" *-- "1" TaskSignals : owns
DownloadTask --|> BaseTask
TaskManager "1" o-- "*" BaseTask : manages
UIMediator ..> TaskManager : observes
UIMediator ..> TaskSignals : connects to UI
@enduml
```

### 🕹️ Sequence Diagram – Submit & Execute

```
@startuml
actor User
participant "UI" as UI
participant "TaskManager" as TM
participant "BaseTask" as Task
participant "TaskSignals" as Signals
participant "QThreadPool" as Pool

User -> UI: click "Start Download"
UI -> TM: submit(downloadTask)
TM -> Task: store in _tasks
TM -> Pool: start(task)
TM -> UI: emit task_added(task)
Pool -> Task: run()
activate Task
Task -> Task: _execute()
loop for each step
    Task -> Task: check is_cancelled()
    alt not cancelled
        Task -> Signals: progress(i)
        Signals --> UI: update progress bar
        Task -> Signals: message("...")
        Signals --> UI: append log
    else cancelled
        Task -> Signals: message("cancelled")
        Signals --> UI: show cancelled
        break
    end
end
Task -> Signals: finished()
deactivate Task
Signals -> TM: finished signal (connected)
TM -> TM: _on_finished() remove task
TM -> UI: task_removed(task_id)
@enduml
```

### 📈 State Diagram – TaskStatus

```
@startuml
[*] --> PENDING : task created
PENDING --> RUNNING : pool.start(task)
RUNNING --> COMPLETED : _execute() success
RUNNING --> FAILED : exception
RUNNING --> CANCELLED : user cancels mid-way
CANCELLED --> [*]
COMPLETED --> [*]
FAILED --> [*]
@enduml
```

Bạn có thể copy các đoạn code PlantUML trên vào [PlantText](https://www.planttext.com/) hoặc dùng extension VS Code để xem biểu đồ.

---

## 🔮 Mở rộng từ đây

- **Hủy an toàn hơn**: Dùng `QEvent` gửi sự kiện dừng qua event loop của worker (nếu worker là QThread). Hiện tại dùng mutex với cờ bool là đủ cho đa số trường hợp.
- **Tạm dừng / Tiếp tục**: Thêm `QMutex` và `QWaitCondition` trong `_execute()`.
- **Ưu tiên task**: Manager có thể sắp xếp pending tasks, nhưng QThreadPool không hỗ trợ ưu tiên sẵn. Ta có thể tự cài đặt hàng đợi riêng và chỉ đẩy task vào pool theo thứ tự ưu tiên.
- **Theo dõi tiến độ tổng hợp**: Tạo một aggregator trong Manager, lắng nghe tất cả task để tính tổng % nếu cần.

Bây giờ bạn đã có khung sườn vững chắc của Cấp độ 3. Hãy thử tự cài đặt một app nhỏ: tải 3 file cùng lúc, mỗi file một progress bar riêng, có nút Cancel. Nếu gặp khó khăn, cứ hỏi mình nhé. Chúc bạn xây dựng framework thành công! 💪