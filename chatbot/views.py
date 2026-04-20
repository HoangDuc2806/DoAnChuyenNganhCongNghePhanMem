# Import các thư viện Django cần thiết
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

# Import model lưu lịch sử chat và sản phẩm
from app.models import ChatHistory, Product

# Thư viện Python cơ bản
import os
import json
import re
from dotenv import load_dotenv

# Import Gemini API mới
from google import genai
from google.genai import types


# ─────────────────────────────────────────────
# LOAD API KEY TỪ FILE .env
# ─────────────────────────────────────────────
load_dotenv()

# Lấy API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Nếu chưa có key → báo lỗi ngay
if not GEMINI_API_KEY:
    raise ValueError("❌ Thiếu GEMINI_API_KEY trong file .env")

# Tạo client kết nối Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# Model bạn đang dùng
GEMINI_MODEL = "gemini-3-flash-preview"


# ─────────────────────────────────────────────
# LẤY DANH SÁCH SẢN PHẨM (CÓ CACHE)
# ─────────────────────────────────────────────
def get_products_cached():
    """
    Lấy sản phẩm từ database và cache lại 5 phút
    → giúp giảm query DB, tăng tốc chatbot
    """
    cached = cache.get("chatbot_products")
    if cached:
        return cached

    # Query DB
    products = Product.objects.prefetch_related('category', 'variants').all()
    result = []

    for p in products:
        # Lấy danh mục
        categories = ', '.join(c.name for c in p.category.all()) or "Chưa phân loại"

        # Lấy biến thể (màu + size còn hàng)
        variants = p.variants.all()
        colors_avail = list({v.color for v in variants if v.stock > 0})
        sizes_avail = sorted({v.size for v in variants if v.stock > 0})

        # Đưa về dạng dict để gửi vào AI
        result.append({
            "id": p.id,
            "name": p.name,
            "price": int(p.price),
            "categories": categories,
            "detail": (p.detail or "")[:120],
            "colors": colors_avail,
            "sizes": sizes_avail,
            "url": f"/detail/?id={p.id}",
        })

    # Cache 300 giây (5 phút)
    cache.set("chatbot_products", result, 300)
    return result


# ─────────────────────────────────────────────
# CHUYỂN SẢN PHẨM THÀNH BẢNG CHO AI
# ─────────────────────────────────────────────
def get_product_table_for_prompt(products):
    """
    Chuyển list sản phẩm → bảng text để đưa vào prompt
    """
    if not products:
        return "Không có sản phẩm."

    # Header bảng
    lines = "| ID | Tên | Danh mục | Giá | Màu | Size | Mô tả |\n"
    lines += "|---|---|---|---|---|---|---|\n"

    for p in products:
        price = f"{p['price']:,}".replace(",", ".")
        colors = ', '.join(p['colors']) or "Liên hệ"
        sizes = ', '.join(p['sizes']) or "Liên hệ"
        desc = p['detail'].replace('|', '')

        lines += f"| {p['id']} | {p['name']} | {p['categories']} | {price}đ | {colors} | {sizes} | {desc} |\n"

    return lines


# ─────────────────────────────────────────────
# SYSTEM PROMPT (LINH HỒN CHATBOT)
# ─────────────────────────────────────────────
def get_system_prompt():
    """
    Prompt hệ thống: định nghĩa cách AI trả lời
    """
    products = get_products_cached()
    table = get_product_table_for_prompt(products)

    return f"""
Bạn là trợ lý bán giày chuyên nghiệp.

DANH SÁCH SẢN PHẨM:
{table}

QUY TẮC:
- Nếu có sản phẩm → thêm:
<<<PRODUCTS:[{{"id":1,"name":"Tên"}}]>>
- Không bịa thông tin
- Trả lời ngắn gọn
"""


# ─────────────────────────────────────────────
# QUẢN LÝ LỊCH SỬ CHAT (SESSION)
# ─────────────────────────────────────────────
MAX_HISTORY = 10

def get_history(session):
    return session.get('chat_history', [])

def save_history(session, history):
    # Giữ tối đa 20 message (10 user + 10 bot)
    session['chat_history'] = history[-20:]
    session.modified = True

def clear_history(session):
    session['chat_history'] = []
    session.modified = True


# ─────────────────────────────────────────────
# CHUYỂN HISTORY → FORMAT GEMINI
# ─────────────────────────────────────────────
def build_contents(history, new_message):
    """
    Convert lịch sử chat sang format API Gemini
    """
    contents = []

    for item in history:
        role = item.get('role', 'user')
        text = item['parts'][0]

        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=text)]
            )
        )

    # Thêm tin nhắn mới của user
    contents.append(
        types.Content(
            role='user',
            parts=[types.Part(text=new_message)]
        )
    )

    return contents


# ─────────────────────────────────────────────
# TÁCH DANH SÁCH SẢN PHẨM TỪ AI
# ─────────────────────────────────────────────
def extract_product_links(reply_text):
    """
    Tìm đoạn <<<PRODUCTS: [...] >>> từ AI trả về
    """
    pattern = r'<<<PRODUCTS:(\[.*?\])>>>'
    match = re.search(pattern, reply_text, re.DOTALL)

    if not match:
        return reply_text, []

    # Xóa đoạn JSON khỏi text hiển thị
    clean_text = re.sub(pattern, '', reply_text).strip()

    try:
        raw_list = json.loads(match.group(1))
        links = [
            {
                "id": i["id"],
                "name": i["name"],
                "url": f"/detail/?id={i['id']}"
            }
            for i in raw_list
        ]
    except:
        links = []

    return clean_text, links


# ─────────────────────────────────────────────
# VIEW HIỂN THỊ GIAO DIỆN
# ─────────────────────────────────────────────
def chatbot_view(request):
    return render(request, 'chatbot/chatbot.html')


# ─────────────────────────────────────────────
# API CHATBOT (CHÍNH)
# ─────────────────────────────────────────────
@csrf_exempt
def chatbot_api(request):
    # Tạo session nếu chưa có
    if not request.session.session_key:
        request.session.create()

    if request.method != 'POST':
        return JsonResponse({'error': 'POST only'}, status=400)

    user_message = request.POST.get('message', '').strip()

    # Nếu user không nhập gì
    if not user_message:
        return JsonResponse({'reply': 'Nhập gì đó đi 😅'})

    history = get_history(request.session)

    try:
        # Nếu là lần đầu → thêm system prompt
        if not history:
            full_message = f"{get_system_prompt()}\n\nUser: {user_message}"
        else:
            full_message = user_message

        # Build nội dung gửi AI
        contents = build_contents(history, full_message)

        # Gọi Gemini API
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=contents,
        )

        # Lấy text trả về
        raw_reply = ""
        if hasattr(response, "text") and response.text:
            raw_reply = response.text.strip()
        else:
            try:
                raw_reply = response.candidates[0].content.parts[0].text.strip()
            except:
                raw_reply = "Lỗi AI 😅"

        # Tách sản phẩm
        clean_reply, product_links = extract_product_links(raw_reply)

        # Lưu history
        history.append({'role': 'user', 'parts': [user_message]})
        history.append({'role': 'model', 'parts': [raw_reply]})
        save_history(request.session, history)

    except Exception as e:
        print("ERROR:", e)
        clean_reply = "Server lỗi 😢"
        product_links = []

    # Lưu DB
    ChatHistory.objects.create(
        user_id=request.session.session_key,
        user_message=user_message,
        bot_reply=clean_reply
    )

    return JsonResponse({
        'reply': clean_reply,
        'product_links': product_links,
    })


# ─────────────────────────────────────────────
# API XÓA LỊCH SỬ CHAT
# ─────────────────────────────────────────────
@csrf_exempt
def chatbot_clear(request):
    if request.method == 'POST':
        clear_history(request.session)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'POST only'})
