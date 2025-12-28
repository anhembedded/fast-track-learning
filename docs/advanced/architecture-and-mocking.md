# Kiến trúc và Quy tắc Mocking

Việc quyết định "nên mock cái gì" và "không nên mock cái gì" là một trong những quyết định khó khăn nhất khi viết test. Một quy tắc sai lầm có thể dẫn đến một bộ test mong manh, khó bảo trì. Câu trả lời nằm ở việc hiểu rõ kiến trúc ứng dụng của bạn.

## Kiến trúc Lục giác (Hexagonal Architecture)

Kiến trúc này chia ứng dụng của bạn thành hai phần chính:

1.  **Lõi ứng dụng (Domain Layer & Application Services Layer):** Đây là nơi chứa toàn bộ logic nghiệp vụ của bạn. Lõi này hoàn toàn không biết gì về thế giới bên ngoài (như database, API, UI).
2.  **Các Adapter:** Là các cổng giao tiếp giúp lõi ứng dụng nói chuyện với thế giới bên ngoài. Ví dụ: một API controller là một adapter nhận request từ HTTP, một repository là một adapter nói chuyện với database.

Mục tiêu của kiến trúc này là **bảo vệ lõi nghiệp vụ khỏi những thay đổi của công nghệ bên ngoài**.

## Phân biệt hai loại Giao tiếp

Đây là chìa khóa để đưa ra quyết định mocking đúng đắn:

1.  **Giao tiếp nội bộ (Intra-system communications):**
    -   **Là gì:** Sự tương tác giữa các class **bên trong** lõi ứng dụng của bạn (ví dụ: `Customer` gọi `Store`).
    -   **Bản chất:** Đây là **chi tiết cài đặt (Implementation Details)**.
    -   **Quy tắc:** **KHÔNG ĐƯỢC MOCK.** Việc mock các giao tiếp nội bộ sẽ khiến test của bạn bị gắn chặt vào thiết kế hiện tại và sẽ bị hỏng khi bạn refactor.

2.  **Giao tiếp liên hệ thống (Inter-system communications):**
    -   **Là gì:** Sự tương tác từ lõi ứng dụng của bạn đi ra một **hệ thống bên ngoài** mà bạn không kiểm soát (ví dụ: gửi email qua SMTP server, gọi API thanh toán của bên thứ ba).
    -   **Bản chất:** Đây là **hành vi quan sát được (Observable Behavior)**.
    -   **Quy tắc:** **NÊN DÙNG MOCK.** Mocking ở đây giúp bạn xác minh rằng ứng dụng của bạn đã tuân thủ đúng "hợp đồng" (contract) khi giao tiếp với thế giới bên ngoài.

### Sơ đồ Quy tắc Mocking

![Hexagonal Architecture Mocking Rule](/images/hexagonal_mocking.png)
*Bạn có thể tạo sơ đồ này bằng mã nguồn `plantuml_sources/hexagonal_mocking.puml`.*

## Cú lừa về Database

Một sai lầm phổ biến là coi **database của chính ứng dụng** là một hệ thống bên ngoài và luôn luôn mock nó.

-   **Database của ứng dụng:** Là database mà chỉ có ứng dụng của bạn sử dụng và bạn có toàn quyền kiểm soát (đổi schema, xóa bảng...). Nó nên được coi là một **chi tiết cài đặt** của ứng dụng. Việc mock nó sẽ làm giảm giá trị của bài test.
-   **Hệ thống bên ngoài:** Là những hệ thống bạn không kiểm soát, như một API của đối tác.

> **Lời khuyên:** Thay vì mock database, hãy viết các bài **Integration Test** chạy trên một database thật (hoặc một phiên bản trong Docker). Điều này sẽ mang lại sự tự tin cao hơn nhiều. Các bài **Unit Test** nên tập trung vào các logic nghiệp vụ thuần túy không phụ thuộc vào I/O.

## Tổng kết: Quy tắc Mocking

| Loại Dependency | Có nên Mock không? | Tại sao? |
| --- | --- | --- |
| Các class khác trong cùng hệ thống | **KHÔNG** | Là chi tiết cài đặt. |
| Database của ứng dụng | **KHÔNG** | Là chi tiết cài đặt. |
| Hệ thống bên ngoài (API, SMTP, etc.) | **CÓ** | Là hành vi quan sát được. |
