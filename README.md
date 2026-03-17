# 🛒 ChatBot Ai Hỗ Trợ Tư Vấn & Bán Hàng

## 📌 Giới thiệu
Đây là hệ thống **Website bán giày trực tuyến** được xây dựng bằng **Django**.  
Hệ thống cho phép người dùng xem sản phẩm, tìm kiếm giày, thêm vào giỏ hàng và thanh toán trực tuyến.

Project được thực hiện trong khuôn khổ **Đồ án chuyên ngành Công nghệ Phần mềm**.

---

# 🚀 Công nghệ sử dụng

- Python 3.12
- Django
- Django REST Framework
- Bootstrap 5
- SQLite
- Stripe Payment API
- Gemini API (Chatbot hỗ trợ khách hàng)

---

# 📂 Cấu trúc Project

Chatbot/
│
├── app/ # Ứng dụng chính (products, orders, services)
│
├── chatbot/ # Chatbot AI
│
├── webbanhang/ # Cấu hình Django
│
├── templates/ # Giao diện HTML
│
├── static/ # CSS / JS / Images
│
├── manage.py
│
└── requirements.txt


---

# ⚙️ Chức năng chính

### 👤 Người dùng
- Đăng ký / Đăng nhập
- Xem danh sách sản phẩm
- Tìm kiếm sản phẩm
- Lọc theo danh mục
- Thêm sản phẩm vào giỏ hàng
- Thanh toán

### 🛠 Admin
- Quản lý sản phẩm
- Quản lý đơn hàng
- Quản lý khách hàng
- Quản lý danh mục

### 🤖 Chatbot AI
- Hỗ trợ khách hàng
- Trả lời câu hỏi về sản phẩm

---

# 🔌 API Endpoints

| Method | Endpoint | Chức năng |
|------|------|------|
| GET | `/api/products/` | Lấy danh sách sản phẩm |
| POST | `/api/products/` | Thêm sản phẩm |
| PUT | `/api/products/{id}/` | Cập nhật sản phẩm |
| DELETE | `/api/products/{id}/` | Xóa sản phẩm |

---

# 🧪 Unit Test

Project có các **unit test cho service layer**:

- Test tạo sản phẩm
- Test cập nhật sản phẩm
- Test xóa sản phẩm
- Test validation dữ liệu
- Test API response

Chạy test:

```bash
python manage.py test

💳 Thanh toán Stripe

Hệ thống tích hợp Stripe Payment Gateway.

Các biến môi trường cần thiết:

STRIPE_PUBLIC_KEY=
STRIPE_SECRET_KEY=

⚙️ Cài đặt project
1️⃣ Clone repository
git clone https://github.com/HoangDuc2806/DoAnChuyenNganhCongNghePhanMem.git

2️⃣ Di chuyển vào thư mục project
cd DoAnChuyenNganhCongNghePhanMem

3️⃣ Tạo virtual environment
python -m venv venv

4️⃣ Cài thư viện
pip install -r requirements.txt

5️⃣ Chạy migrate
python manage.py migrate

6️⃣ Chạy server
python manage.py runserver


Truy cập:

http://127.0.0.1:8000
