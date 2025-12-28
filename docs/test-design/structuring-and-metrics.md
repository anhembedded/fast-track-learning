# Cấu trúc và Đánh giá Test

Sau khi nắm được các khái niệm cơ bản, bước tiếp theo là tìm hiểu cách cấu trúc một bài test cho dễ đọc và cách đánh giá bộ test của bạn một cách đúng đắn.

## Mẫu AAA — Arrange / Act / Assert

Đây là một mẫu cấu trúc (pattern) cực kỳ phổ biến giúp cho các bài test trở nên rõ ràng và nhất quán. Một bài test nên được chia thành 3 phần riêng biệt:

1.  **Arrange (Sắp đặt):**
    -   **Mục đích:** Chuẩn bị mọi thứ cần thiết để bài test có thể chạy.
    -   **Công việc:** Khởi tạo đối tượng, chuẩn bị dữ liệu đầu vào, thiết lập các mock/stub.

2.  **Act (Hành động):**
    -   **Mục đích:** Thực thi hành vi (behavior) mà bạn muốn kiểm tra.
    -   **Công việc:** Gọi phương thức hoặc hàm cần test. Thông thường, phần này chỉ nên có một dòng code duy nhất.

3.  **Assert (Xác minh):**
    -   **Mục đích:** Kiểm tra xem kết quả của hành động có đúng như mong đợi hay không.
    -   **Công việc:** So sánh kết quả trả về hoặc trạng thái của đối tượng với một giá trị kỳ vọng.

### Sơ đồ tuần tự của mẫu AAA

Sơ đồ này minh họa luồng hoạt động của một bài test theo mẫu AAA.

![AAA Pattern Sequence](/images/aaa_pattern_sequence.png)

*Bạn có thể tìm thấy mã nguồn của sơ đồ này tại `plantuml_sources/aaa_pattern_sequence.puml` để tự render.*

## Các chỉ số Độ bao phủ (Coverage Metrics) — Hiểu cho đúng

Độ bao phủ (code coverage) là một chỉ số đo lường tỷ lệ code của bạn được thực thi bởi các bài test. Tuy nhiên, đây là một chỉ số rất dễ bị hiểu sai.

-   **Line coverage (Độ phủ dòng lệnh):** Tỷ lệ phần trăm số dòng code đã được chạy qua bởi bộ test.
-   **Branch coverage (Độ phủ nhánh):** Tỷ lệ phần trăm các nhánh quyết định (ví dụ: `if/else`, `switch/case`) đã được thực thi. Đây là chỉ số quan trọng hơn line coverage.

### Công thức tính Branch Coverage

> Branch coverage = (Số nhánh đã được test chạy qua) / (Tổng số nhánh trong mã nguồn)

### Coverage là một chỉ báo, không phải mục tiêu

Hãy nhớ rằng, coverage là một công cụ để tìm ra những phần code **chưa được test**, chứ không phải là thước đo chất lượng của bộ test.

-   **Coverage thấp (ví dụ: < 50%):** Chắc chắn là một dấu hiệu xấu. Điều này có nghĩa là một phần lớn code của bạn chưa hề được kiểm tra.
-   **Coverage cao (ví dụ: 90-100%):** **Không đảm bảo** rằng bộ test của bạn tốt. Một bài test có thể chạy qua 100% dòng code nhưng lại thiếu các `assert` quan trọng, hoặc chỉ kiểm tra những thứ tầm thường.

> **Lời khuyên:** Đừng đuổi theo con số coverage. Hãy tập trung vào việc viết những bài test có ý nghĩa, kiểm tra các logic nghiệp vụ quan trọng.
