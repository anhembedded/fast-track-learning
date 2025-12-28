# Chào mừng đến với Wiki Unit Test

Đây là trang tài liệu tổng hợp các kiến thức, nguyên tắc và bài học thực tế về Unit Testing trong phát triển phần mềm. Mục tiêu của trang wiki này là biến những kiến thức phức tạp thành một nguồn tài liệu **dễ học, dễ tra cứu** cho các lập trình viên.

## Tóm tắt cốt lõi

- **Unit testing là một mạng lưới an toàn (safety net)** giúp phát hiện lỗi hồi quy (regressions) và duy trì tốc độ phát triển của dự án về lâu dài.
- Nếu code của bạn **khó để viết unit test**, đó thường là một dấu hiệu của thiết kế kém (ví dụ: tight coupling - liên kết chặt chẽ). Ngược lại, code dễ test không đảm bảo rằng đó là code hoàn hảo.
- **Mục tiêu chính khi viết test:**
    1.  Phát hiện lỗi hồi quy một cách hiệu quả.
    2.  Giảm chi phí bảo trì bộ test.
    3.  Cho phép tái cấu trúc (refactor) code một cách an toàn và tự tin.
- **Không có test:** Dự án có thể phát triển nhanh lúc đầu, nhưng sẽ chậm lại đáng kể về sau do sự entropy của mã nguồn (code ngày càng phức tạp, rối rắm và dễ hỏng).
- **Có test:** Việc sửa đổi và tái cấu trúc code trở nên an toàn hơn, giúp dự án duy trì được chất lượng và tốc độ.

## Triết lý

> Code không phải là một tài sản (asset), nó là một khoản nợ (liability). Code càng nhiều, rủi ro tiềm ẩn bug càng lớn. Unit test chính là "tấm khiên" bảo vệ bạn khỏi khoản nợ đó.

Hãy bắt đầu khám phá các chủ đề chi tiết hơn qua thanh điều hướng bên trái!
