<div align="center">

# 👟 Shop Giày DLN

**Website bán giày trực tuyến tích hợp Chatbot AI**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.1-092E20?logo=django&logoColor=white)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![Gemini](https://img.shields.io/badge/Gemini_AI-3.0_Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> Đồ án chuyên ngành · Công nghệ Phần mềm

[Tính năng](#-tính-năng) · [Công nghệ](#️-công-nghệ) · [Cài đặt](#-cài-đặt) · [API](#-api) · [Cấu trúc](#-cấu-trúc-thư-mục)

</div>

---

## 📌 Giới thiệu

**Shop Giày DLN** là website thương mại điện tử chuyên bán giày, xây dựng bằng Django framework. Hệ thống cho phép khách hàng duyệt sản phẩm, tìm kiếm, quản lý giỏ hàng, đặt hàng và nhận tư vấn trực tiếp từ **Chatbot AI** tích hợp Google Gemini.

Dự án được thực hiện nhằm áp dụng các kiến thức về phân tích thiết kế hệ thống, lập trình web, cơ sở dữ liệu, bảo mật và quản lý dự án theo Sprint.

---

## ✨ Tính năng

### 👤 Khách hàng
| Tính năng | Mô tả |
|---|---|
| Đăng ký / Đăng nhập | Xác thực người dùng bằng Django Authentication |
| Duyệt sản phẩm | Xem danh sách, lọc theo danh mục, xem chi tiết |
| Chọn màu & size | Chọn biến thể sản phẩm (màu sắc, size, tồn kho) |
| Tìm kiếm thông minh | Tìm theo tên, gợi ý tự động khi gõ |
| Giỏ hàng | Thêm, cập nhật số lượng, xóa sản phẩm |
| Đặt hàng | Checkout, nhập địa chỉ giao hàng, tạo hóa đơn |
| Thanh toán | COD hoặc thanh toán online qua **Stripe** |
| Lịch sử giao dịch | Xem các đơn hàng đã đặt và trạng thái duyệt |

### 🤖 Chatbot AI
| Tính năng | Mô tả |
|---|---|
| Tư vấn sản phẩm | Gợi ý giày phù hợp theo nhu cầu người dùng |
| Nhớ ngữ cảnh | Duy trì lịch sử hội thoại trong session |
| Link sản phẩm | Hiển thị chip bấm được dẫn thẳng đến trang chi tiết |
| Thông tin cửa hàng | Trả lời về giá, chính sách, giờ làm việc |
| Xử lý lỗi | Phản hồi thân thiện khi API gặp sự cố |

### 🔐 Bảo mật
- Mã hóa mật khẩu qua Django Authentication
- CSRF Token cho tất cả form POST
- API Key và thông tin nhạy cảm lưu trong `.env`
- Ẩn secrets khỏi GitHub bằng `.gitignore`

---

## 🛠️ Công nghệ

| Nhóm | Công nghệ |
|---|---|
| **Backend** | Python 3.12, Django 5.1, Django REST Framework |
| **Frontend** | HTML5, CSS3, Bootstrap 5.3, JavaScript ES6 |
| **Database** | SQLite (development) / MySQL (production) |
| **AI** | Google Gemini API 1.5 Flash |
| **Thanh toán** | Stripe |
| **Dev Tools** | Git, GitHub, Postman, python-dotenv |

---

## 🗄️ Cơ sở dữ liệu

```
User ──────────────── Order ──────── OrderItem ──── Product
 │                      │                               │
 │                      │                            Category (M2M)
 │                 ShippingAddress                      │
 │                      │                          ProductVariant
 └──────────────── Invoice                        (màu, size, tồn kho)

ChatHistory  ←  lưu lịch sử hội thoại chatbot
```

| Model | Mô tả |
|---|---|
| `User` | Tài khoản người dùng (Django built-in) |
| `Category` | Danh mục sản phẩm, hỗ trợ danh mục con |
| `Product` | Sản phẩm: tên, giá, ảnh, mô tả, danh mục |
| `ProductVariant` | Biến thể sản phẩm: màu sắc, size, tồn kho |
| `Order` | Đơn hàng với trạng thái: pending / approved / canceled |
| `OrderItem` | Chi tiết từng dòng trong đơn hàng |
| `ShippingAddress` | Địa chỉ giao hàng của đơn |
| `Invoice` | Hóa đơn liên kết 1-1 với Order |
| `ChatHistory` | Lịch sử hội thoại chatbot |

---

## 🚀 Cài đặt

### Yêu cầu
- Python 3.10+
- pip

### 1. Clone repository

```bash
git clone https://github.com/your-username/shop-giay-dln.git
cd shop-giay-dln
```

### 2. Tạo môi trường ảo và cài dependencies

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường

Tạo file `.env` ở thư mục gốc:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_django_secret_key_here
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
DEBUG=True
```

### 4. Chạy migration và tạo superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Khởi động server

```bash
python manage.py runserver
```

Truy cập tại: `http://127.0.0.1:8000`  
Admin panel: `http://127.0.0.1:8000/admin`

---

## 🔗 API

### Sản phẩm

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/api/products/` | Lấy danh sách sản phẩm |
| `GET` | `/api/products/<id>/` | Xem chi tiết sản phẩm |
| `POST` | `/api/products/create/` | Tạo sản phẩm mới |
| `DELETE` | `/api/products/delete/<id>/` | Xóa sản phẩm |

### Giỏ hàng & Đặt hàng

| Method | Endpoint | Mô tả |
|---|---|---|
| `POST` | `/update_item/` | Thêm / giảm / xóa sản phẩm trong giỏ |
| `GET/POST` | `/checkout/` | Xác nhận đặt hàng |
| `GET` | `/create-checkout-session/` | Tạo phiên thanh toán Stripe |

### Chatbot

| Method | Endpoint | Mô tả |
|---|---|---|
| `POST` | `/chatbot/api/` | Gửi tin nhắn đến chatbot |
| `POST` | `/chatbot/clear/` | Xóa lịch sử hội thoại |

**Ví dụ request chatbot:**

```bash
curl -X POST http://127.0.0.1:8000/chatbot/api/ \
  -d "message=Tôi muốn mua giày chạy bộ"
```

**Response:**

```json
{
  "reply": "Chào bạn! Shop có các mẫu giày chạy bộ...",
  "product_links": [
    { "id": 1, "name": "Adizero SL2", "url": "/detail/?id=1" },
    { "id": 2, "name": "Nike Air Max", "url": "/detail/?id=2" }
  ]
}
```

---

## 📂 Cấu trúc thư mục

```
Chatbot/
│
├── app/                        # App chính — sản phẩm, đơn hàng, người dùng
│   ├── migrations/             # Database migrations
│   ├── templates/app/          # HTML templates
│   ├── static/app/             # CSS, JS, images
│   ├── templatetags/           # Custom template filters (vnd_filters)
│   ├── models.py               # Product, Order, Invoice, Variant...
│   ├── views.py                # Logic xử lý request
│   ├── urls.py                 # URL routing
│   ├── admin.py                # Cấu hình Django Admin
│   └── serializers.py          # DRF serializers cho API
│
├── chatbot/                    # App chatbot AI
│   ├── templates/chatbot/
│   ├── views.py                # Xử lý Gemini API + lịch sử hội thoại
│   └── urls.py
│
├── webbanhang/                 # Cấu hình project Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── db.sqlite3                  # Database SQLite
├── manage.py
├── requirements.txt
├── .env                        # ← KHÔNG commit lên Git
├── .gitignore
└── README.md
```

---

## 📸 Giao diện

| Trang | Mô tả |
|---|---|
| Trang chủ | Banner, danh mục, sản phẩm nổi bật, chatbot |
| Danh mục | Lọc theo brand, hiển thị grid sản phẩm |
| Chi tiết | Ảnh lớn, chọn màu / size, thêm giỏ hàng |
| Giỏ hàng | Danh sách sản phẩm, tổng tiền, đặt hàng |
| Thanh toán | Form giao hàng + tóm tắt đơn hàng |
| Lịch sử | Danh sách đơn đã đặt, trạng thái, xem hóa đơn |

---

## 👨‍💻 Tác giả

**Shop Giày DLN** — Đồ án chuyên ngành Công nghệ Phần mềm

> Nếu có câu hỏi, vui lòng mở Issue hoặc liên hệ qua email của nhóm.

---

<div align="center">
  <sub>Built with ❤️ using Django + Google Gemini AI</sub>
</div>
