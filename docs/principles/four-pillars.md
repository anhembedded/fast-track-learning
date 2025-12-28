# Bốn trụ cột của một Unit Test tốt

Để một bài test thực sự có giá trị, nó không chỉ cần tìm ra lỗi. Một bài test tốt phải cân bằng giữa việc phát hiện lỗi và chi phí bảo trì nó. Tác giả Vladimir Khorikov đã định nghĩa một hệ thống gồm bốn trụ cột để đánh giá chất lượng của một unit test.

Một bài test tốt phải đứng vững trên cả bốn trụ cột này:

1.  **Protection against regressions (Bảo vệ khỏi lỗi hồi quy)**
2.  **Resistance to refactoring (Chống chịu được tái cấu trúc)**
3.  **Fast feedback (Phản hồi nhanh)**
4.  **Maintainability (Dễ bảo trì)**

---

## Trụ cột 1: Bảo vệ khỏi lỗi hồi quy

Đây là mục đích cơ bản nhất của mọi bài test.

-   **Lỗi hồi quy (Regression) là gì?** Là khi một tính năng đang hoạt động bình thường bỗng dư-ng bị hỏng sau khi bạn thay đổi code ở một nơi khác.
-   **Làm sao để một bài test có khả năng bảo vệ tốt?**
    -   **Thực thi nhiều code:** Bài test chạy qua càng nhiều logic nghiệp vụ thì khả năng phát hiện lỗi càng cao.
    -   **Kiểm tra code phức tạp:** Test một thuật toán phức tạp có giá trị hơn là test một hàm getter/setter đơn giản.
    -   **Tập trung vào nghiệp vụ cốt lõi:** Test các logic quan trọng như thanh toán, phân quyền sẽ có giá trị cao hơn.
-   **Lời khuyên:** Đừng lãng phí thời gian test những đoạn code tầm thường (trivial code) không chứa logic.

---

## Trụ cột 2: Chống chịu được tái cấu trúc

Đây là trụ cột quan trọng nhất và thường bị bỏ qua nhất, quyết định chi phí bảo trì của bộ test.

-   **Tái cấu trúc (Refactoring) là gì?** Là việc thay đổi cấu trúc code bên trong (ví dụ: tối ưu thuật toán, đổi tên biến) mà **không làm thay đổi hành vi có thể quan sát được bên ngoài**.
-   **Báo động giả (False Positive):** Nếu bạn tái cấu trúc code mà bài test bị "đỏ" (fail), trong khi chức năng vẫn đúng, thì bài test đó đã tạo ra một báo động giả.
-   **Tại sao báo động giả lại nguy hiểm?**
    -   **Mất niềm tin:** Khi test báo lỗi giả quá nhiều, lập trình viên sẽ dần mất tin tưởng vào bộ test. Họ sẽ bắt đầu lờ đi các cảnh báo, và đó là lúc lỗi thật sự (true positive) sẽ bị bỏ lọt.
    -   **Ngại thay đổi:** Một bộ test "mong manh" (brittle) sẽ cản trở việc tái cấu trúc, khiến cho codebase ngày càng xuống cấp.
-   **Làm sao để test chống chịu được tái cấu trúc?** Hãy kiểm tra **"Cái gì" (What - kết quả cuối cùng)** thay vì **"Làm thế nào" (How - các bước thực hiện bên trong)**.

---

## Trụ cột 3: Phản hồi nhanh

Tốc độ là yếu tố quyết định tần suất bạn chạy bộ test.

-   **Vòng lặp phản hồi (Feedback Loop):** Test càng nhanh, bạn càng có thể chạy chúng thường xuyên hơn. Điều này giúp bạn phát hiện lỗi ngay khi nó vừa được tạo ra, làm cho việc sửa lỗi trở nên dễ dàng và ít tốn kém hơn rất nhiều.
-   **Phân biệt Unit Test và Integration Test:** Đây chính là yếu tố khác biệt lớn nhất. Unit test phải chạy trong vài mili giây, trong khi integration test có thể mất vài giây hoặc hơn.

---

## Trụ cột 4: Dễ bảo trì

Code test cũng quan trọng như code sản phẩm. Một bài test khó đọc, khó chạy sẽ trở thành gánh nặng.

-   **Độ khó hiểu:**
    -   **Ngắn gọn:** Một bài test nên ngắn gọn và tập trung vào một kịch bản duy nhất.
    -   **Dễ đọc:** Sử dụng các mẫu như AAA, đặt tên test rõ ràng để thể hiện ý định.
-   **Độ khó vận hành:**
    -   Một unit test tốt phải có thể chạy mà không cần một môi trường phức tạp (không cần database, không cần server, không cần file cấu hình).

---

## Sự đánh đổi

Không thể có một bài test hoàn hảo đạt điểm tối đa ở cả 4 trụ cột. Sẽ luôn có sự đánh đổi, đặc biệt là giữa **Trụ cột 1 (Bảo vệ)** và **Trụ cột 2 (Chống chịu refactor) & 3 (Tốc độ)**.

-   **E2E Test:** Bảo vệ tốt nhất, chống chịu refactor tốt, nhưng phản hồi cực kỳ chậm.
-   **Unit Test mong manh:** Bảo vệ tốt, phản hồi nhanh, nhưng chống chịu refactor cực tệ.
-   **Unit Test tốt:** Cân bằng giữa cả bốn yếu tố, trong đó **khả năng chống chịu refactor và dễ bảo trì là không thể nhân nhượng**.
