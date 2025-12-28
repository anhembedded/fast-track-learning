# Hướng dẫn Cập nhật và Quản lý Wiki

Chào bạn, đây là tài liệu hướng dẫn giúp bạn tự mình mở rộng và cập nhật nội dung cho trang Dev Unit Test Wiki.

---

## 1. Cách thêm Nội dung và Mục điều hướng Mới

Trang wiki này là một ứng dụng trang đơn (Single Page Application - SPA). Tất cả nội dung đều nằm trong file `index.html`. Mỗi phần nội dung tương ứng với một thẻ `<section>` và một mục trên thanh điều hướng (`<nav>`).

**Để thêm một mục mới, bạn cần làm 2 bước:**

### Bước 1: Thêm mục vào thanh điều hướng (Sidebar)

Mở file `index.html` và tìm đến phần `<nav class="sidebar">`. Bạn sẽ thấy một danh sách `<ul>` với các thẻ `<li>`.

Để thêm một mục mới, hãy sao chép một thẻ `<li>` có sẵn và chỉnh sửa nó.

-   `data-target`: Đây là **ID định danh duy nhất** cho mục mới của bạn. Hãy đặt một tên không trùng lặp (ví dụ: `my-new-topic`).
-   `data-feather`: Tên của icon. Bạn có thể chọn icon từ trang [Feather Icons](https://feathericons.com/).
-   Bên trong thẻ `<span>`: Đây là tên sẽ hiển thị trên thanh điều hướng.

**Ví dụ:** Thêm mục "Chủ đề mới của tôi"

```html
<!-- ... các mục nav khác ... -->
<li class="nav-category">Chủ đề Mới</li>
<li class="nav-item" data-target="my-new-topic">
    <i data-feather="plus-circle"></i>
    <span>Chủ đề mới của tôi</span>
</li>
<!-- ... -->
```

### Bước 2: Thêm nội dung tương ứng

Bây giờ, hãy kéo xuống phần `<main class="main-content">`. Bạn sẽ thấy nhiều thẻ `<section>` ở đây.

Hãy sao chép một thẻ `<section>` có sẵn và chỉnh sửa nó.

-   `id`: **ID này phải khớp chính xác** với giá trị `data-target` bạn đã đặt ở Bước 1 (ví dụ: `my-new-topic`).
-   Bên trong thẻ `<section>`: Đây là nơi bạn đặt toàn bộ nội dung HTML cho chủ đề mới của mình (tiêu đề, đoạn văn, danh sách, hình ảnh, v.v.).

**Ví dụ:** Thêm nội dung cho "Chủ đề mới của tôi"

```html
<!-- ... các section khác ... -->
<section id="my-new-topic" class="content-section">
    <h1>Đây là Chủ đề Mới Của Tôi</h1>
    <p>Nội dung chi tiết về chủ đề này.</p>
    <ul>
        <li>Mục 1</li>
        <li>Mục 2</li>
    </ul>
</section>
<!-- ... -->
```

Sau khi lưu file `index.html`, trang wiki sẽ tự động cập nhật với mục và nội dung mới của bạn.

---

## 2. Cách thêm Từ khóa vào Từ điển (Glossary)

Hệ thống tooltip và trang từ điển được quản lý hoàn toàn tự động từ file `js/main.js`.

### Bước 1: Thêm định nghĩa vào `glossaryData`

Mở file `js/main.js`. Ngay trên đầu file, bạn sẽ thấy một đối tượng tên là `glossaryData`.

Để thêm một từ mới, hãy thêm một cặp `key: value` vào đối tượng này.

-   **Key:** Là một chuỗi định danh duy nhất, viết thường, dùng dấu gạch ngang (ví dụ: `new-keyword`).
-   **Value:** Là một đối tượng chứa 2 thuộc tính:
    -   `short`: Định nghĩa ngắn gọn sẽ hiển thị trong tooltip.
    -   `long`: Định nghĩa chi tiết sẽ hiển thị trên trang Từ điển.

**Ví dụ:** Thêm từ "New Keyword"

```javascript
const glossaryData = {
    // ... các từ khóa khác
    'new-keyword': {
        short: "Đây là định nghĩa ngắn gọn cho tooltip.",
        long: "Đây là định nghĩa dài và chi tiết hơn sẽ xuất hiện trên trang Glossary."
    },
    // ...
};
```

### Bước 2: Đánh dấu từ khóa trong HTML

Trong file `index.html`, tìm đến từ bạn muốn biến thành từ khóa và bọc nó trong thẻ `<span>` như sau:

```html
<p>Đây là một câu có chứa <span class="keyword" data-keyword="new-keyword">New Keyword</span>.</p>
```

-   `class="keyword"`: Bắt buộc phải có để hệ thống nhận diện.
-   `data-keyword`: **Phải khớp chính xác** với "Key" bạn đã định nghĩa trong `glossaryData` ở Bước 1.

Vậy là xong! Trang web sẽ tự động tạo tooltip và thêm mục mới vào trang Từ điển.

---

## 3. Cách thêm Sơ đồ UML

Các sơ đồ trong trang được gợi ý tạo từ mã nguồn PlantUML để dễ dàng quản lý và chỉnh sửa.

### Bước 1: Viết mã PlantUML

1.  Tạo một thư mục tên là `plantuml_sources` ở thư mục gốc của dự án nếu nó chưa tồn tại.
2.  Tạo một file mới với đuôi `.puml` (ví dụ: `my_diagram.puml`) trong thư mục đó.
3.  Viết mã nguồn PlantUML của bạn vào file này.

### Bước 2: Tạo ảnh từ mã PlantUML

Bạn có thể tạo ảnh `.png` hoặc `.svg` từ file `.puml` bằng nhiều cách:

-   **Online Editor:** Truy cập [PlantUML Web Server](http://www.plantuml.com/plantuml), dán code của bạn vào và xuất ra file ảnh.
-   **VS Code Extension:** Cài đặt extension "PlantUML" trong VS Code. Mở file `.puml` và dùng tính năng preview/export của extension.
-   **Local Jar:** Tải file `plantuml.jar` về máy và chạy lệnh command-line để tạo ảnh.

### Bước 3: Chèn ảnh vào Wiki

1.  Lưu file ảnh bạn vừa tạo vào thư mục `images/`.
2.  Trong file `index.html`, chèn ảnh bằng thẻ `<img>` như bình thường.

**Ví dụ:**

```html
<img src="images/my_diagram.png" alt="Mô tả sơ đồ của tôi">
<p><em>Bạn có thể tạo sơ đồ này bằng mã nguồn <code>plantuml_sources/my_diagram.puml</code>.</em></p>
```

---

## 4. Cách sử dụng Tính năng Tô màu Code (Syntax Highlighting)

Trang wiki đã được tích hợp sẵn thư viện **Prism.js** để tự động tô màu cho các khối mã.

Để sử dụng, bạn chỉ cần bọc code của mình trong cặp thẻ `<pre><code class="...">...</code></pre>` và chỉ định đúng ngôn ngữ lập trình.

-   Class của thẻ `<code>` phải có dạng `language-{tên ngôn ngữ}`.
-   Một số tên ngôn ngữ phổ biến: `python`, `javascript`, `java`, `csharp`, `html`, `css`, `bash`.

**Ví dụ cho Python:**

```html
<pre><code class="language-python">
# Đây là code Python
def hello(name):
    print(f"Hello, {name}!")

hello("World")
</code></pre>
```

**Ví dụ cho JavaScript:**

```html
<pre><code class="language-javascript">
// Đây là code JavaScript
function greet(name) {
    console.log(`Hello, ${name}!`);
}

greet('World');
</code></pre>
```

Prism.js sẽ tự động phát hiện và tô màu cho khối mã đó.
