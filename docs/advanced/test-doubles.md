# Mocks, Stubs và Test Doubles

Khi viết unit test, chúng ta cần "cách ly" đơn vị đang được test (SUT - System Under Test) khỏi các dependency (đối tượng phụ thuộc) của nó. **Test Doubles** là thuật ngữ chung chỉ các đối tượng giả được tạo ra để thay thế các dependency thật trong môi trường test.

Mặc dù chúng ta hay gọi chung là "mock", nhưng có nhiều loại Test Double khác nhau, mỗi loại có một mục đích riêng. Phân biệt rõ chúng là chìa khóa để viết các bài test đúng đắn.

## Stub (Giả lập dữ liệu)

-   **Mục đích:** Cung cấp dữ liệu đầu vào (input) cho SUT để nó có thể chạy. Stub giúp mô phỏng các trạng thái và giá trị khác nhau.
-   **Vai trò:** Đóng vai trò "người cung cấp thông tin". SUT sẽ **lấy dữ liệu từ** Stub.
-   **Quy tắc vàng:** **Đừng bao giờ xác minh (verify) một lời gọi đến Stub.** Việc SUT gọi Stub một hay nhiều lần không quan trọng, miễn là kết quả cuối cùng đúng. Việc verify Stub sẽ khiến test bị gắn chặt vào chi tiết cài đặt.

```python
from unittest.mock import Mock

# database_stub là một Stub vì nó cung cấp dữ liệu cho SUT
database_stub = Mock()
database_stub.get_user.return_value = {"name": "Alice", "email": "alice@example.com"}

# SUT sẽ sử dụng dữ liệu này để thực hiện logic
user_service = UserService(database_stub)
```

## Mock (Giả lập hành động)

-   **Mục đích:** Giả lập và xác minh các tương tác đi ra (outcoming interaction) từ SUT đến các hệ thống bên ngoài.
-   **Vai trò:** Đóng vai trò "người nhận lệnh". SUT sẽ **gửi lệnh đến** Mock.
-   **Cách dùng:** Sau khi hành động (Act) diễn ra, bạn sẽ xác minh (verify) xem SUT đã gọi đúng phương thức của Mock với đúng tham số hay chưa.

```python
from unittest.mock import Mock

# email_sender_mock là một Mock vì nó nhận lệnh từ SUT
email_sender_mock = Mock()

user_service = UserService(email_sender_mock)
user_service.register("alice@example.com")

# Xác minh rằng SUT đã gửi lệnh đi đúng cách
email_sender_mock.send_welcome_email.assert_called_with("alice@example.com")
```

## Phân biệt qua Nguyên lý CQS (Command-Query Separation)

Một cách tuyệt vời để phân biệt khi nào dùng Stub và khi nào dùng Mock là dựa vào nguyên lý CQS:

-   **Query (Truy vấn):** Một phương thức trả về giá trị nhưng không làm thay đổi trạng thái hệ thống.
    -   Các dependency dạng Query nên được thay thế bằng **Stub**.
-   **Command (Lệnh):** Một phương thức làm thay đổi trạng thái hệ thống (side effect) nhưng không trả về giá trị (void).
    -   Các dependency dạng Command nên được thay thế bằng **Mock**.

## Các loại Test Double khác

-   **Dummy:** Một đối tượng được truyền vào chỉ để lấp đầy danh sách tham số, nhưng không bao giờ được sử dụng thực sự.
-   **Fake:** Một đối tượng có một phiên bản cài đặt hoạt động thực sự, nhưng đơn giản hơn nhiều so với bản production (ví dụ: in-memory database thay vì một database thật).
-   **Spy:** Một đối tượng vừa đóng vai trò là Stub (cung cấp dữ liệu), vừa ghi lại thông tin về các lời gọi đến nó (giống Mock). Spy thường được dùng để bao bọc một đối tượng thật.

> **Lưu ý:** Các thư viện như `unittest.mock` của Python hay `Moq` của C# thường cung cấp một class `Mock` đa năng. Bạn có thể sử dụng class này để tạo ra cả Stub, Mock, và Spy. Điều quan trọng là **cách bạn sử dụng** đối tượng đó trong bài test sẽ quyết định vai trò thực sự của nó.
