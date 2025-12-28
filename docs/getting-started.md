# Bắt đầu với Unit Test

Phần này sẽ giới thiệu những khái niệm nền tảng nhất mà bạn cần nắm vững trước khi đi sâu vào các kỹ thuật chi tiết.

## ✅ Test Tốt vs. Test Tồi

Một bài test được coi là **"tốt"** khi nó mang lại giá trị cao với chi phí bảo trì thấp. Ngược lại, một bài test **"tồi"** sẽ trở thành gánh nặng cho dự án.

-   **Test Tốt:**
    -   Chạy nhanh.
    -   Mục đích rõ ràng, dễ đọc.
    -   Độc lập, không phụ thuộc vào các test khác.
    -   Ít chi phí bảo trì khi code thay đổi (chống chịu được refactor).
    -   Tập trung vào các hành vi (behavior) quan trọng của hệ thống.

-   **Test Tồi:**
    -   Chạy chậm.
    -   Dễ bị "vỡ" (fail) dù logic của ứng dụng vẫn đúng.
    -   Có nhiều code thừa (boilerplate).
    -   Gây ra các cảnh báo giả (false positive), làm mất niềm tin của lập trình viên.
    -   Bị trùng lặp (redundant) với các test khác.

## Phân loại các cấp độ Test

Trong phát triển phần mềm, có nhiều cấp độ kiểm thử khác nhau, mỗi loại có một mục đích riêng. Ba loại phổ biến nhất thường được minh họa qua mô hình Kim tự tháp Kiểm thử.

1.  **Unit Test (Kiểm thử đơn vị):**
    -   **Mục tiêu:** Kiểm tra một đơn vị (unit) code nhỏ và cô lập (ví dụ: một hàm, một class).
    -   **Đặc điểm:** Chạy hoàn toàn trong bộ nhớ (in-memory), không phụ thuộc vào các hệ thống bên ngoài như database, file system hay network. Rất nhanh.

2.  **Integration Test (Kiểm thử tích hợp):**
    -   **Mục tiêu:** Kiểm tra sự tương tác và phối hợp giữa hai hay nhiều thành phần của hệ thống, hoặc giữa hệ thống của bạn và một hệ thống bên ngoài (database, API của bên thứ ba).
    -   **Đặc điểm:** Chậm hơn Unit Test vì cần truy cập vào các tài nguyên ngoài process.

3.  **End-to-end (E2E) Test (Kiểm thử đầu-cuối):**
    -   **Mục tiêu:** Kiểm tra toàn bộ luồng hoạt động của ứng dụng từ góc nhìn của người dùng cuối.
    -   **Đặc điểm:** Mô phỏng một người dùng thật, tương tác từ giao diện người dùng (UI) xuống tới database. Rất chậm và chi phí bảo trì cao.

## Mô hình Kim tự tháp Kiểm thử (Test Pyramid)

Đây là một mô hình trực quan giúp định hướng chiến lược viết test: hãy viết thật nhiều Unit Test, ít hơn Integration Test và số lượng E2E Test là ít nhất.

![Test Pyramid](/images/test_pyramid.png)

*Bạn có thể tìm thấy mã nguồn của sơ đồ này tại `plantuml_sources/test_pyramid.puml` để tự render.*
