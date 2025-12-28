# Các mẫu (Patterns) xử lý dữ liệu Test

Khi viết unit test, phần `Arrange` (chuẩn bị dữ liệu) thường là phần dài dòng và lặp đi lặp lại nhất. Nếu không được quản lý tốt, nó có thể làm cho các bài test trở nên khó đọc và khó bảo trì. Dưới đây là một số mẫu thiết kế phổ biến giúp bạn giải quyết vấn đề này.

## Vấn đề: Phần `Arrange` quá dài

Hãy xem xét một ví dụ với các model `Customer`, `Order`, `Item`.

```python
# models.py
class Item:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

class Customer:
    def __init__(self, first_name: str, is_vip: bool = False):
        self.first_name = first_name
        self.is_vip = is_vip

class Order:
    def __init__(self, customer: Customer):
        self.customer = customer
        self.items = []

    def add_item(self, item: Item):
        self.items.append(item)

    @property
    def total(self) -> float:
        return sum(i.price for i in self.items)

    def apply_discount(self):
        if self.customer.is_vip:
            # VIP: 10% off
            total = self.total
            return round(total * 0.9, 2)
        return round(self.total, 2)
```

Một bài test thông thường có thể trông như thế này:

```python
# test_standard.py
from models import Item, Customer, Order

def test_order_total_with_discount_standard():
    # ARRANGE (rất nhiều chi tiết, không phải tất cả đều quan trọng)
    customer = Customer(first_name="Hoang", is_vip=True)
    order = Order(customer)
    order.add_item(Item("Laptop", 1000))
    order.add_item(Item("Mouse", 50))

    # ACT
    discounted_price = order.apply_discount()

    # ASSERT
    assert discounted_price == 945.0
```

Trong bài test trên, các chi tiết như `"Hoang"`, `"Laptop"`, `"Mouse"` không thực sự quan trọng đối với logic cần test (logic giảm giá cho khách VIP). Chúng làm cho bài test bị "nhiễu".

## Mẫu 1: Object Mother

**Ý tưởng:** Tạo một class "Mẹ" chứa các phương thức `static` để tạo ra các phiên bản phổ biến của một đối tượng.

```python
# test_object_mother.py
from models import Item, Order

class CustomerMother:
    @staticmethod
    def vip():
        from models import Customer
        return Customer(first_name="VIP Customer", is_vip=True)

    @staticmethod
    def regular():
        from models import Customer
        return Customer(first_name="Regular Customer", is_vip=False)

def test_order_total_with_object_mother():
    # ARRANGE (gọn gàng hơn, che giấu chi tiết không cần thiết)
    customer = CustomerMother.vip()
    order = Order(customer)
    order.add_item(Item("Laptop", 1000))

    # ACT
    discounted_price = order.apply_discount()

    # ASSERT
    assert discounted_price == 900.0
```

-   **Ưu điểm:** Nhanh, gọn, dễ sử dụng cho các trường hợp phổ biến.
-   **Nhược điểm:** Kém linh hoạt. Nếu bạn cần một khách hàng VIP nhưng có tên khác, bạn sẽ phải thêm một phương thức mới hoặc sửa đổi đối tượng sau khi tạo.

## Mẫu 2: Test Data Builder

**Ý tưởng:** Tạo một class `Builder` với một API linh hoạt (fluent interface) cho phép bạn tùy chỉnh các thuộc tính của đối tượng một cách dễ dàng.

```python
# test_builder.py
from models import Item, Order

class CustomerBuilder:
    def __init__(self):
        self._first_name = "Default Name"
        self._is_vip = False

    def with_vip(self, is_vip: bool):
        self._is_vip = is_vip
        return self

    def with_name(self, name: str):
        self._first_name = name
        return self

    def build(self):
        from models import Customer
        return Customer(first_name=self._first_name, is_vip=self._is_vip)

def test_order_with_builder():
    # ARRANGE (linh hoạt và rất dễ đọc)
    customer = CustomerBuilder().with_vip(True).with_name("An").build()
    order = Order(customer)
    order.add_item(Item("Pen", 10))

    # ACT
    discounted_price = order.apply_discount()

    # ASSERT
    assert discounted_price == 9.0
```

-   **Ưu điểm:** Rất linh hoạt, dễ đọc, thể hiện rõ ý định của bài test (chỉ những thuộc tính được tùy chỉnh mới quan trọng).
-   **Nhược điểm:** Cần viết nhiều code hơn một chút để tạo builder.

## Khi nào nên dùng mẫu nào?

-   **Object Mother:** Phù hợp cho các đối tượng đơn giản, có ít biến thể và được sử dụng rộng rãi.
-   **Test Data Builder:** Là lựa chọn tốt nhất cho các đối tượng phức tạp hoặc khi bạn cần nhiều biến thể khác nhau trong các bài test. Đây thường là mẫu được ưu tiên trong các dự án lớn.
