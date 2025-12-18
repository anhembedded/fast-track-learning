# Summary

- **Unit testing as a negative indicator**:

  - If code is **hard to unit test**, it usually signals poor design.
  - Common cause: **tight coupling** between components, making them difficult to isolate and test separately.
  - In this sense, difficulty in testing highlights areas needing improvement.
- **Unit testing as a positive indicator**:

  - The fact that code is **easy to unit test** does **not automatically mean** the code is well-designed.
  - Good testability doesn’t guarantee good quality — code could still be inefficient, poorly structured, or flawed in other ways.

---

- **Goal of unit testing**:To enable **sustainable growth** of a software project — keeping development speed steady over time rather than slowing down as complexity increases.
- **Without tests**:

  - Projects start fast but slow down drastically as code grows.
  - This slowdown is caused by **software entropy** — code deteriorates with each change, becoming more complex and fragile.
  - Fixing one bug often introduces others, leading to instability and unreliability.
- **With tests**:

  - Unit tests act as a **safety net**, preventing regressions (features breaking after modifications).
  - They ensure existing functionality continues to work even after new features or refactoring.
  - This stabilizes the code base and supports long-term scalability.
- **Trade-off**:

  - Writing tests requires significant upfront effort.
  - However, they **pay off in the long run** by reducing maintenance costs and allowing projects to grow sustainably.
- **Key concepts**:

  - **Regression** = a bug introduced when previously working functionality breaks after code changes.
  - **Sustainability & scalability** = the ultimate goals of unit testing, ensuring projects can evolve without collapsing under their own complexity.

---

## ✅ What Makes a Good Test

* **Catches regressions reliably**
  * Detects when existing functionality breaks after changes.
  * Provides confidence to refactor or add features.
* **Low maintenance cost**
  * Easy to update when production code changes.
  * Doesn’t require constant rewriting or debugging.
* **Clear and readable**
  * Serves as documentation for how the code is supposed to behave.
  * Developers can quickly understand intent without confusion.
* **Fast execution**
  * Runs quickly so developers can use them continuously (e.g., in CI/CD pipelines).
  * Encourages frequent feedback loops.
* **Focused and independent**
  * Tests one thing at a time.
  * Doesn’t rely on external systems or other tests (avoids flakiness).

---

## ❌ What Makes a Bad Test

* **Raises false alarms**
  * Fails even when the code is correct, wasting developer time.
  * Leads to mistrust in the test suite.
* **High upkeep cost**
  * Needs frequent refactoring whenever production code changes.
  * Adds more work than value.
* **Slow and brittle**
  * Takes too long to run, discouraging frequent use.
  * Breaks easily due to dependencies or fragile setups.
* **Unclear purpose**
  * Hard to read or understand.
  * Doesn’t clearly show what behavior is being validated.
* **Redundant or excessive**
  * Tests the same thing multiple times without adding new value.
  * Adds unnecessary code that increases maintenance burden.

---

## 1. 🎯 What Are Coverage Metrics?

* **Definition** : A coverage metric tells you how much of your source code is executed by your test suite.
* Range: **0% (no code tested)** →  **100% (every line executed at least once)** .
* Two common types:
  * **Code coverage (line coverage)** → % of lines executed.
  * **Branch coverage** → % of decision paths (`if/else`, `switch`) executed.

## 4. ⚖️ Why Coverage Metrics Are Limited

* **Good negative indicator** :
* Low coverage (e.g., 10%) → clear sign you’re not testing enough.
* **Bad positive indicator** :
* High coverage (even 100%) → doesn’t guarantee good tests.
* Tests might be shallow, redundant, or miss important scenarios.

## 5. 🧠 Key Takeaways

* Coverage metrics are  **feedback tools** , not quality guarantees.
* Don’t chase a number (like “we must hit 90% coverage”).
* Focus on **valuable tests** that:
  * Catch regressions.
  * Cover meaningful branches and outcomes.
  * Are easy to maintain.

Alright Anh, let’s turn this into a **tutorial-style explanation** so you can really understand **branch coverage** and how it differs from code coverage.  

---

# 📘 Tutorial: Understanding Branch Coverage

## 1. 🎯 What Is Branch Coverage?
- **Branch coverage** measures how many **decision paths** in your code are executed by tests.  
- Focuses on **control structures** like `if`, `else`, `switch`, and loops.  
- Formula:  

\[
\text{Branch coverage} = \frac{\text{Branches traversed by tests}}{\text{Total branches in code}}
\]

👉 Unlike **code coverage** (which counts lines), branch coverage checks whether **all possible outcomes** of decisions are tested.

---

## 5. 🧠 Key Takeaways
- **Branch coverage > code coverage** in precision.  
- It ensures **all decision outcomes** are tested.  
- But like code coverage, it’s still just a metric — high branch coverage doesn’t guarantee good test quality.  
- The real goal: write tests that **catch regressions and validate behavior**, not just chase numbers.

---

## 5. 🧠 Key Takeaways
- Coverage metrics are **helpful indicators**, but not reliable measures of test quality.  
- Problems:
  1. They don’t guarantee all outcomes are verified.  
  2. They can be gamed with assertion-free tests.  
  3. They ignore hidden paths in external libraries.  
- **Successful test suites** focus on:
  - Meaningful assertions.  
  - Covering important branches and edge cases.  
  - Preventing regressions, not chasing numbers.

---

## 5. 🧠 Key Takeaways
A **successful test suite**:
1. **Integrated** → runs continuously in the dev cycle.  
2. **Focused** → targets the most critical parts of the system (domain model).  
3. **Efficient** → provides maximum value with minimum maintenance cost.  

👉 It’s not about quantity or coverage numbers. It’s about **quality, trust, and sustainability**.

Ok, giờ mình làm **đúng thứ bạn cần** 👌
Dưới đây là **MỘT BÀI HỌC HOÀN CHỈNH**, có **cấu trúc để tự học**, có **ví dụ xuyên suốt**, và **xoay đúng vào trục duy nhất** mà bạn chỉ ra:

> **Khi test một unit, bạn muốn cô lập nó tới mức nào?**

Không lan man framework, không sa đà thuật ngữ, đọc theo thứ tự là hiểu.

---

# BÀI HỌC: CÔ LẬP TỚI ĐÂU KHI VIẾT UNIT TEST?

---

## 1. Điểm xuất phát của mọi unit test

Khi bạn viết unit test cho một hàm hay một class, bạn đang tự hỏi (dù có ý thức hay không):

> “Mình cho phép những thứ nào cùng chạy với đoạn code này trong lúc test?”

Câu hỏi này quan trọng hơn cả:

* dùng framework gì
* có mock hay không
* assert kiểu nào

Bởi vì **mức độ cô lập** chính là thứ quyết định tất cả những điều đó.

---

## 2. Ví dụ xuyên suốt: Dịch vụ xử lý đơn hàng

Giả sử có một class `OrderService` với nhiệm vụ:

* Nhận yêu cầu đặt hàng
* Kiểm tra kho
* Trừ hàng
* Trả về kết quả thành công hay thất bại

Để làm được việc này, `OrderService` cần dùng:

* `Inventory` (quản lý số lượng)
* `PaymentGateway` (xử lý thanh toán)

Câu hỏi đặt ra:

> Khi test `OrderService`, ta cho phép `Inventory` và `PaymentGateway` chạy thật hay không?

---

## 3. Lựa chọn 1: Cô lập khỏi môi trường (Classical)

Ở lựa chọn này, bạn nói:

> “Tôi chấp nhận cho các class nghiệp vụ chạy cùng nhau, miễn là không đụng tới môi trường bên ngoài.”

### Cách test diễn ra

* Tạo `Inventory` thật
* Tạo `PaymentGateway` giả lập đơn giản (không gọi API thật)
* Gọi `OrderService.PlaceOrder`
* Kiểm tra:

  * đơn hàng thành công hay không
  * số lượng hàng trong kho có giảm không

### Ví dụ minh họa (ý tưởng)

```text
Trước test: kho có 10 sản phẩm
Đặt mua 3 sản phẩm
Sau test: kho còn 7 sản phẩm
Kết quả: thành công
```

### Bản chất của kiểu test này

* Test dựa trên **trạng thái cuối cùng**
* Nhiều class cùng tham gia
* Test giống hành vi thật của hệ thống

Isolation ở đây nghĩa là:

> Không phụ thuộc database, network, hệ điều hành

---

## 4. Hệ quả tự nhiên của Classical style

* Test có thể fail vì nhiều nguyên nhân
* Khó xác định chính xác class nào sai
* Nhưng:

  * test dễ đọc
  * test ít bị vỡ khi refactor
  * phù hợp với domain logic

Nếu bạn thay đổi cách `OrderService` gọi `Inventory` bên trong, miễn là kết quả cuối cùng vẫn đúng, test vẫn pass.

---

## 5. Lựa chọn 2: Cô lập khỏi mọi dependency (London)

Ở lựa chọn này, bạn nói:

> “Tôi chỉ muốn test `OrderService`. Mọi thứ khác đều là nhiễu.”

### Cách test diễn ra

* `Inventory` → mock
* `PaymentGateway` → mock
* Test quyết định:

  * khi hỏi còn hàng → trả lời có
  * khi gọi trừ hàng → ghi nhận lời gọi

### Ví dụ minh họa (ý tưởng)

```text
Giả sử Inventory nói: còn đủ hàng
Khi đặt hàng:
- OrderService phải gọi Inventory.Remove(quantity)
- PaymentGateway.Charge() phải được gọi 1 lần
```

### Bản chất của kiểu test này

* Test dựa trên **hành vi giao tiếp**
* Không có state thật
* Không có logic thật ở dependency

Isolation ở đây nghĩa là:

> Class đang test chạy hoàn toàn một mình

---

## 6. Sự khác biệt cốt lõi thể hiện ở ASSERT

| Classical            | London                        |
| -------------------- | ----------------------------- |
| Kho còn bao nhiêu?   | Có gọi RemoveInventory không? |
| Đơn hàng thành công? | Có gọi Charge() không?        |
| Trạng thái sau cùng  | Tương tác xảy ra              |

Chỉ cần nhìn vào assert là biết test thuộc trường phái nào.

---

## 7. Từ mức độ cô lập → mọi thứ khác tự xuất hiện

Khi bạn chọn **Classical**:

* Không cần mock nhiều
* Không cần interface phức tạp
* Assert vào state

Khi bạn chọn **London**:

* Bắt buộc có interface
* Bắt buộc có mock
* Assert vào interaction

Mock không phải mục tiêu, mock chỉ là **hệ quả**.

---

## 8. Khi nào nên chọn mức cô lập nào?

### Nghiêng về Classical khi:

* Logic nghiệp vụ rõ ràng
* Ít dependency
* Muốn test giống thực tế
* Muốn test sống lâu với refactor

### Nghiêng về London khi:

* Class có nhiều dependency
* Object graph phức tạp
* Muốn pinpoint lỗi chính xác
* Muốn ép kiến trúc rõ ràng

---

## 9. Bài tập tự học (rất quan trọng)

Lấy bất kỳ class nào bạn đang có và tự hỏi:

1. Class này phụ thuộc vào những gì?
2. Nếu dependency này sai, tôi có muốn test fail không?
3. Tôi đang quan tâm **kết quả cuối cùng** hay **cách nó được thực hiện**?

Câu trả lời cho 3 câu này sẽ tự động nói cho bạn:

* nên dùng Classical hay London
* có cần mock hay không
* assert vào đâu

---

## 10. Kết luận của bài học

Toàn bộ unit test **không xoay quanh mock hay framework**.

Nó xoay quanh **một quyết định duy nhất**:

> **Khi test một unit, bạn muốn cô lập nó tới mức nào?**

* Cô lập khỏi môi trường → Classical
* Cô lập khỏi mọi dependency → London

Từ quyết định đó, mọi thứ còn lại **tự động hợp lý**.

---

Nếu bạn muốn bước tiếp theo, mình có thể:

* Viết **bài học tiếp theo: Cách quyết định mock hay không trong 30 giây**
* Hoặc **viết lại toàn bộ bằng Python**
* Hoặc **liên hệ sang tư duy test cho embedded / firmware**

Bạn chỉ cần nói hướng bạn muốn đi tiếp.
