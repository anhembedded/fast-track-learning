# Behavior vs. Implementation Details

Để viết được những bài test có khả năng chống chịu tái cấu trúc (resistant to refactoring), bạn buộc phải hiểu rõ và phân biệt được đâu là **hành vi quan sát được** và đâu là **chi tiết cài đặt**.

-   **Kiểm tra hành vi quan sát được:** Giúp bài test của bạn trở nên bền vững.
-   **Kiểm tra chi tiết cài đặt:** Khiến bài test của bạn trở nên mong manh (brittle).

## Định nghĩa

Mọi đoạn code đều có thể được phân loại theo hai góc nhìn:

1.  **Góc nhìn Công khai (Public vs. Private):**
    -   **Public API:** Các phương thức và thuộc tính mà code bên ngoài (client) được phép truy cập.
    -   **Private API:** Các phương thức và thuộc tính chỉ được sử dụng trong nội bộ của class.

2.  **Góc nhìn Mục đích (Behavior vs. Implementation):**
    -   **Hành vi quan sát được (Observable Behavior):** Là những kết quả hoặc tác dụng phụ (side effect) mà client mong đợi khi tương tác với đối tượng. Đây là "cái gì" (what) mà code của bạn làm.
    -   **Chi tiết cài đặt (Implementation Details):** Là các bước, thuật toán, hoặc cấu trúc dữ liệu nội bộ được sử dụng để tạo ra hành vi đó. Đây là "làm thế nào" (how) mà code của bạn thực hiện công việc.

### Mối quan hệ

Một API được thiết kế tốt (well-designed) là khi **Public API và Observable Behavior là một**. Tất cả các chi tiết cài đặt phải được che giấu (encapsulated) và là `private`.

![Well-designed API vs. Leaking API](/images/api_design.png)
*Bạn có thể tạo sơ đồ này bằng mã nguồn `plantuml_sources/api_design.puml`.*

Khi một chi tiết cài đặt bị "rò rỉ" (leak) ra Public API, nó sẽ cám dỗ bạn viết những bài test kiểm tra vào đó, và đó là nguồn gốc của các bài test mong manh.

## Ví dụ: Rò rỉ Logic

Hãy xem xét một class `User` cần đảm bảo tên người dùng không dài quá 50 ký tự.

### 🔴 Cách làm sai (Rò rỉ)

Logic chuẩn hóa tên (`normalize_name`) bị để ở dạng `public`.

```python
# BAD CODE: Logic chuẩn hóa bị rò rỉ
class User:
    def __init__(self, name=""):
        self.name = name

    # Đây là chi tiết cài đặt, nhưng lại là public!
    def normalize_name(self, name):
        # ... logic cắt chuỗi ...

class UserController:
    def rename_user(self, user, new_name):
        # Client phải biết quá nhiều về "làm thế nào"
        normalized = user.normalize_name(new_name)
        user.name = normalized
```

-   **Vấn đề:** Client phải gọi 2 phương thức để hoàn thành một mục tiêu. Nếu một client khác quên gọi `normalize_name`, hệ thống sẽ có dữ liệu không nhất quán.

### 🟢 Cách làm đúng (Đóng gói)

Logic chuẩn hóa được giấu vào bên trong và trở thành `private`.

```python
# GOOD CODE: Đóng gói hoàn toàn
class User:
    def __init__(self, name=""):
        self.name = name # Setter sẽ tự động gọi logic chuẩn hóa

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = self._normalize_name(value)

    # Chi tiết cài đặt thực sự
    def _normalize_name(self, name):
        # ... logic cắt chuỗi ...

class UserController:
    def rename_user(self, user, new_name):
        # Client chỉ cần biết "cái gì", không cần biết "làm thế nào"
        user.name = new_name
```

-   **Lợi ích:** Bây giờ bạn có thể thay đổi hoàn toàn logic `_normalize_name` mà không làm hỏng `UserController` hoặc các bài test của nó.

## Nguyên lý Tell, Don't Ask

Nguyên lý này là kim chỉ nam giúp bạn thiết kế API tốt:

-   **Ask (Hỏi - Xấu):** Hỏi một đối tượng về trạng thái của nó, thực hiện logic ở bên ngoài, rồi cập nhật lại trạng thái cho đối tượng đó. (Đây là ví dụ sai ở trên).
-   **Tell (Bảo - Tốt):** Ra lệnh cho một đối tượng thực hiện một hành động. Đối tượng sẽ tự sử dụng trạng thái nội bộ của nó để thực hiện hành động đó. (Đây là ví dụ đúng ở trên).

Bằng cách tuân thủ "Tell, Don't Ask", bạn sẽ tự động tạo ra các API đóng gói tốt, che giấu các chi tiết cài đặt và giúp cho các bài test của bạn trở nên bền vững hơn.
