## 📌 Giới thiệu dự án
**Shop Giày DLN** là website bán giày trực tuyến được xây dựng bằng **Django**.  
Hệ thống hỗ trợ khách hàng xem sản phẩm, tìm kiếm, thêm vào giỏ hàng, đặt hàng, theo dõi lịch sử mua hàng và sử dụng **Chatbot AI** để tư vấn sản phẩm.

Dự án được thực hiện nhằm phục vụ cho **đồ án chuyên ngành Công nghệ Phần mềm**.

---

## 🎯 Mục tiêu dự án
- Xây dựng website bán giày trực tuyến thân thiện, dễ sử dụng.
- Hỗ trợ khách hàng tìm kiếm và mua sản phẩm nhanh chóng.
- Tích hợp chatbot AI để tư vấn, hỗ trợ mua hàng.
- Áp dụng các kiến thức về:
  - Phân tích thiết kế hệ thống
  - Lập trình Web với Django
  - Cơ sở dữ liệu
  - Bảo mật ứng dụng Web
  - Quản lý dự án phần mềm theo Sprint

---

## 🛠️ Công nghệ sử dụng

### Backend
- **Python**
- **Django**
- **Django REST Framework**

### Frontend
- **HTML**
- **CSS**
- **Bootstrap 5**
- **JavaScript**

### Database
- **SQLite** *(có thể thay bằng MySQL nếu cần)*

### Công cụ khác
- **Git & GitHub**
- **Postman** (test API)
- **Google Gemini API** *(Chatbot AI - nếu có dùng)*
- **dotenv (.env)**

---

## ✨ Chức năng chính

### 👤 Người dùng
- Đăng ký tài khoản
- Đăng nhập / Đăng xuất
- Xem danh sách sản phẩm
- Xem chi tiết sản phẩm
- Tìm kiếm sản phẩm
- Lọc sản phẩm theo danh mục
- Thêm sản phẩm vào giỏ hàng
- Cập nhật số lượng sản phẩm
- Xóa sản phẩm khỏi giỏ hàng
- Thanh toán đơn hàng
- Xem lịch sử giao dịch

### 🤖 Chatbot AI
- Hỏi đáp tự động
- Gợi ý sản phẩm
- Hỗ trợ khách hàng mua hàng
- Có thể thêm sản phẩm vào giỏ từ chatbot

### 🔐 Bảo mật
- Mật khẩu được mã hóa bằng Django Authentication
- Dùng CSRF Token cho các form POST
- Dùng file `.env` để lưu API Key / Secret
- Ẩn thông tin nhạy cảm khỏi GitHub bằng `.gitignore`

---

## 📂 Cấu trúc thư mục dự án

```bash
Chatbot/
│
├── app/                    # Ứng dụng chính
│   ├── migrations/
│   ├── templates/
│   │   └── app/
│   ├── static/
│   │   └── app/
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── serializers.py
│   └── templatetags/
│
├── chatbot/                # Cấu hình project Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── media/                  # Lưu hình ảnh upload
├── static/                 # Static files tổng
├── templates/              # Template tổng (nếu có)
├── db.sqlite3              # Database SQLite
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

🗄️ Cơ sở dữ liệu chính

Hệ thống có các bảng dữ liệu chính như:

User → Quản lý tài khoản người dùng
Customer → Thông tin khách hàng
Category → Danh mục sản phẩm
Product → Thông tin sản phẩm
Order → Đơn hàng
OrderItem → Chi tiết đơn hàng
ShippingAddress → Địa chỉ giao hàng

🔗 API Endpoint chính
Sản phẩm
GET /api/products/ → Lấy danh sách sản phẩm
POST /api/products/create/ → Tạo sản phẩm mới
DELETE /api/products/delete/<id>/ → Xóa sản phẩm
GET /api/products/<id>/ → Xem chi tiết sản phẩm
Chatbot
POST /chatbot/api/ → Gửi câu hỏi đến chatbot
Giỏ hàng
POST /update_item/ → Thêm / giảm / xóa sản phẩm trong giỏ
