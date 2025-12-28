# Hai trường phái Unit Testing: London vs. Classical

Trong cộng đồng phát triển phần mềm, có hai trường phái tư duy chính về cách tiếp cận unit testing, đặc biệt là về vấn đề "cách ly" (isolation) và việc sử dụng các đối tượng giả (test doubles).

## Trường phái London (còn gọi là Mockist)

-   **Triết lý:** Một "unit" (đơn vị) được kiểm thử là một **class duy nhất**. Mọi dependency (đối tượng phụ thuộc) của class đó, dù là một class khác trong hệ thống của bạn, đều phải được thay thế bằng mock.
-   **Tập trung vào Tương tác (Interaction):** Các bài test theo trường phái này xác minh xem class đang được test (SUT - System Under Test) có gọi đúng các phương thức của dependency hay không. Đây được gọi là *interaction testing*.
-   **Ưu điểm:**
    -   Khi một bài test fail, bạn biết chính xác class nào đang bị lỗi.
    -   Không cần phải khởi tạo một đồ thị đối tượng (object graph) phức tạp.
-   **Nhược điểm:**
    -   Các bài test bị **gắn chặt vào chi tiết cài đặt (implementation details)**. Nếu bạn refactor code bằng cách thay đổi cách các class tương tác với nhau (nhưng vẫn giữ đúng kết quả cuối cùng), các bài test sẽ bị hỏng (false positive). Điều này làm tăng đáng kể chi phí bảo trì.

## Trường phái Classical (còn gọi là Detroit hoặc Classicist)

-   **Triết lý:** Một "unit" là một **hành vi nghiệp vụ (unit of behavior)**. Nó có thể bao gồm một class hoặc một nhóm các class làm việc cùng nhau để hoàn thành một nhiệm vụ.
-   **Tập trung vào Kết quả (State):** Các bài test theo trường phái này kiểm tra kết quả cuối cùng hoặc sự thay đổi trạng thái của hệ thống sau khi hành động được thực hiện. Đây được gọi là *state testing*.
-   **Cách ly:** Trường phái này định nghĩa "cách ly" là việc các **bài test phải độc lập với nhau**. Test A không được ảnh hưởng đến kết quả của Test B.
-   **Sử dụng Test Doubles:** Chỉ sử dụng mock/stub cho các **dependency thực sự bên ngoài và chậm**, như network, database, file system (được gọi là *shared dependencies*). Các class thông thường trong cùng một hệ thống được sử dụng trực tiếp.
-   **Ưu điểm:**
    -   Các bài test có khả năng **chống chịu refactoring cao**. Bạn có thể tự do thay đổi cấu trúc code nội bộ miễn là kết quả đầu ra không đổi.
    -   Bộ test phản ánh đúng hơn giá trị nghiệp vụ của ứng dụng.
-   **Nhược điểm:**
    -   Khi một bài test fail, có thể khó xác định ngay lập-tức class nào gây ra lỗi.

## Lời khuyên

Cả hai trường phái đều có ưu và nhược điểm riêng. Tuy nhiên, để xây dựng một bộ test bền vững và ít chi phí bảo trì, **trường phái Classical thường được ưu tiên hơn**. Việc các bài test có khả năng chống chịu refactoring là một trong những yếu tố quan trọng nhất của một bộ test tốt.

> **Quan trọng:** Hãy chọn một phong cách nhất quán cho toàn bộ đội nhóm và tuân thủ nó. Việc trộn lẫn hai phong cách này trong cùng một codebase có thể dẫn đến những cuộc tranh cãi không cần thiết và làm cho bộ test trở nên khó hiểu.
