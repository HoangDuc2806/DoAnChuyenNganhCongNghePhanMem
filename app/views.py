# ====================================================================
# 1. KHAI BÁO THƯ VIỆN (IMPORTS)
# Gom toàn bộ các thư viện từ trên xuống dưới lên đầu file để dễ quản lý
# ====================================================================

# Thư viện chuẩn của Python
import json

# Thư viện bên thứ ba (Stripe, Django REST framework)
import stripe
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Các module cốt lõi của Django
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.timezone import now, localtime

# Các module từ ứng dụng (models, serializers)
from .models import * # Import toàn bộ model (Product, Order, OrderItem, Category, Invoice...)
from app.models import Product  # Dòng này hơi thừa vì đã có import * ở trên, nhưng giữ nguyên theo logic cũ
from .serializers import ProductSerializer

# Cấu hình khóa bí mật cho Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


# ==============================================================================
# 2. XÁC THỰC NGƯỜI DÙNG (AUTHENTICATION)
# Các hàm xử lý Đăng ký, Đăng nhập, Đăng xuất
# ==============================================================================

def register(request):
    # Khởi tạo form đăng ký người dùng trống
    form = CreateUserForm() 
    
    # Nếu người dùng gửi dữ liệu lên (nhấn nút Đăng ký)
    if request.method == "POST":
        # Điền dữ liệu POST vào form
        form = CreateUserForm(request.POST)
        user_not_login = "hidden" # Ẩn nút đăng nhập/đăng ký
        user_login = "show"       # Hiện thông tin người dùng
        
        # Kiểm tra tính hợp lệ của dữ liệu form
        if form.is_valid():
            form.save()           # Lưu tài khoản mới vào database
            return redirect('login') # Chuyển hướng đến trang đăng nhập
            
    # Mặc định trạng thái hiển thị cho khách (chưa đăng nhập)
    user_not_login = "show"
    user_login = "hidden"
    
    # Kiểm tra giỏ hàng để hiển thị trên thanh điều hướng (header)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        
    # Chuẩn bị dữ liệu gửi ra giao diện
    context = {
        'form': form,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'app/register.html', context)


def loginPage(request):
    # Nếu đã đăng nhập thì tự động chuyển về trang chủ
    if request.user.is_authenticated:
        return redirect('home')
    
    # Xử lý khi người dùng gửi form đăng nhập
    if request.method == "POST":
        username = request.POST.get('username') # Lấy tên đăng nhập
        password = request.POST.get('password') # Lấy mật khẩu
        # Dùng hàm authenticate của Django để kiểm tra thông tin
        user = authenticate(request, username=username, password=password)
        
        user_not_login = "hidden"
        user_login = "show"
        
        if user is not None:
            login(request, user)  # Tạo session đăng nhập cho user
            return redirect('home') # Chuyển hướng về trang chủ
        else:
            # Báo lỗi nếu sai tài khoản/mật khẩu
            messages.info(request, 'user or password not correct!')
            
    # Lấy thông tin giỏ hàng để hiển thị trên giao diện
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        
    # Setup trạng thái hiển thị cho khách
    user_not_login = "show"
    user_login = "hidden"
    
    context = { 
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    return render(request, 'app/login.html', context)


def logoutPage(request):
    # Xóa session đăng nhập của người dùng
    logout(request)
    # Chuyển hướng về lại trang đăng nhập
    return redirect('login')


# ==============================================================================
# 3. TRANG CHÍNH & TÌM KIẾM (MAIN PAGES & SEARCH)
# Trang chủ, Trang danh mục, Chi tiết sản phẩm, Tìm kiếm
# ==============================================================================

def home(request):
    # Kiểm tra trạng thái đăng nhập để hiển thị giỏ hàng
    if request.user.is_authenticated:
        customer = request.user
        # Lấy giỏ hàng đang mở (complete=False), nếu chưa có thì tạo mới
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # Lấy tất cả sản phẩm trong giỏ
        cartItems = order.get_cart_items  # Lấy tổng số lượng sản phẩm
        user_not_login = "hidden"
        user_login = "show"
    else:
        # Giả lập dữ liệu trống nếu chưa đăng nhập
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0} 
        cartItems = 0 
        user_not_login = "show"
        user_login = "hidden"
        
    # Lấy danh sách danh mục cha (không phải danh mục con)
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','') # Trạng thái danh mục đang chọn

    products = Product.objects.all()  # Lấy toàn bộ sản phẩm từ DB
    
    context = {
        'categories': categories,
        'active_category': active_category,
        'products': products,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    return render(request, 'app/home.html', context)


def category(request):
    # Lấy danh sách danh mục cha để hiển thị menu
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')  # Lấy tham số 'category' từ URL (slug)

    # Nếu URL có tham số danh mục (vd: ?category=ao-thun)
    if active_category:
        # Tìm danh mục có slug tương ứng
        categories_with_slug = Category.objects.filter(slug=active_category)
        # Lấy các sản phẩm thuộc danh mục đó
        products = Product.objects.filter(category__in=categories_with_slug) 
    else:
        # Không chọn gì thì lấy tất cả sản phẩm
        products = Product.objects.all() 

    # Cập nhật số lượng giỏ hàng trên giao diện header
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        user_not_login = "show"
        user_login = "hidden"
        customer = None  # Đảm bảo 'customer' tồn tại
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
        'categories': categories,
        'products': products,
        'active_category': active_category
    }
    return render(request, 'app/category.html', context)


def detail(request):
    # Lấy dữ liệu giỏ hàng để render thanh header
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        user_not_login = "show"
        user_login = "hidden"

    # Lấy ID sản phẩm từ URL (vd: ?id=5)
    id = request.GET.get('id', '')
    product = Product.objects.get(id=id)  # ✅ Lấy đối tượng sản phẩm chính từ DB

    # ✅ Lấy các sản phẩm tương tự (cùng danh mục, trừ chính sản phẩm đang xem, giới hạn 4 cái)
    related_products = Product.objects.filter(
        category__in=product.category.all()
    ).exclude(id=product.id)[:4]

    # Lấy danh mục để hiển thị menu
    categories = Category.objects.filter(is_sub=False)

    context = {
        'products': [product],          # Bọc trong list để tương thích với template cũ
        'related_products': related_products,  # ✅ Danh sách sản phẩm tương tự
        'categories': categories,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    return render(request, 'app/detail.html', context)


def search(request):
    searched = ''  # Đảm bảo biến luôn tồn tại
    keys = []      # Danh sách kết quả tìm kiếm rỗng mặc định

    # Xử lý khi có form tìm kiếm gửi lên
    if request.method == "POST":
        searched = request.POST["searched"]  # Lấy từ khóa từ thẻ input form
        # Lọc sản phẩm có tên chứa từ khóa (không phân biệt hoa/thường - icontains)
        keys = Product.objects.filter(name__icontains=searched) 

    # Lấy giỏ hàng cho Header
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items 
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0} 
        cartItems = 0 
        user_not_login = "show"
        user_login = "hidden"

    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()  # Lấy tất cả làm nền hoặc đề xuất thêm
    
    return render(request, 'app/search.html', {
        "searched": searched,
        "keys": keys,
        'categories': categories,
        'products': products,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    })


def search_suggestions(request):
    # Xử lý AJAX gợi ý tìm kiếm
    query = request.GET.get('term', '').strip() # Lấy từ khóa đang gõ
    suggestions = []

    if query:
        # Giới hạn lấy 5 sản phẩm khớp đầu tiên
        products = Product.objects.filter(name__icontains=query)[:7] 
        # Đóng gói kết quả thành danh sách dict (JSON chuẩn)
        suggestions = [{'id': p.id, 'name': p.name} for p in products]

    # Trả về chuỗi JSON, cho phép list không bọc trong dict (safe=False)
    return JsonResponse(suggestions, safe=False)


# ==============================================================================
# 4. GIỎ HÀNG, CHECKOUT & HÓA ĐƠN (CART, CHECKOUT & INVOICES)
# ==============================================================================

def cart(request):
    # Lấy thông tin giỏ hàng
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # Các dòng sản phẩm
        cartItems = order.get_cart_items  # Tổng số sản phẩm
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = 0
        user_not_login = "show"
        user_login = "hidden"
        
    categories = Category.objects.filter(is_sub=False)
    
    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login
    }
    return render(request, 'app/cart.html', context)


def updateItem(request):
    # Hàm xử lý AJAX thao tác: Thêm, Bớt, Xóa sản phẩm trong giỏ
    data = json.loads(request.body)  # Đọc dữ liệu JSON gửi từ file JS
    productId = data['productId']    # ID của sản phẩm cần thao tác
    action = data['action']          # Loại hành động (add, remove, delete)
    
    print('Action:', action)
    print('Product:', productId)

    customer = request.user # Chỉ dùng được khi người dùng đã đăng nhập
    product = Product.objects.get(id=productId) # Lấy đối tượng sản phẩm từ DB

    # Lấy giỏ hàng hiện tại (chưa thanh toán)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    # Tìm xem sản phẩm này đã có trong giỏ hàng chưa
    orderItem = OrderItem.objects.filter(order=order, product=product).first()

    # Nếu chưa có trong giỏ và hành động không phải là 'delete' -> Tạo mới
    if not orderItem and action != 'delete':
        orderItem = OrderItem.objects.create(order=order, product=product, quantity=0)

    # Cập nhật số lượng dựa trên action
    if action == 'add':
        orderItem.quantity += 1 # Thêm 1
        orderItem.save()
        
    elif action == 'remove':
        orderItem.quantity -= 1 # Giảm 1
        if orderItem.quantity <= 0:
            orderItem.delete()  # Xóa luôn nếu số lượng về 0
        else:
            orderItem.save()
            
    elif action == 'delete':
        if orderItem:
            orderItem.delete()  # Xóa hoàn toàn khỏi giỏ
            print(f"🗑️ Deleted product {productId} from cart")
        else:
            print("⚠️ Tried to delete non-existent item")

    # Trả về JSON tổng số sản phẩm mới cập nhật để JS render lại số trên logo giỏ
    cart_items = order.get_cart_items if hasattr(order, 'get_cart_items') else 0
    return JsonResponse({'message': 'Cart updated', 'cart_items': cart_items})


def checkout(request):
    # Lấy thông tin user hiện tại nếu họ đã đăng nhập, ngược lại gán bằng None
    user = request.user if request.user.is_authenticated else None
    
    # Thiết lập biến chuỗi để ẩn/hiện các thành phần giao diện (HTML) dựa trên trạng thái đăng nhập
    user_not_login = "hidden" if user else "show"
    user_login = "show" if user else "hidden"

    # Khởi tạo các biến mặc định cho giỏ hàng
    cartItems = 0
    order = None
    items = []

    # Nếu người dùng đã đăng nhập
    if user:
        try:
            # Tìm giỏ hàng hiện tại (đơn hàng chưa hoàn tất: complete=False)
            order = Order.objects.get(customer=user, complete=False)
            # Lấy danh sách tất cả các sản phẩm có trong giỏ hàng này
            items = order.orderitem_set.all()
            # Lấy tổng số lượng sản phẩm trong giỏ hàng (sử dụng property/phương thức của model)
            cartItems = order.get_cart_items
        except Order.DoesNotExist:
            # Nếu không tìm thấy giỏ hàng nào đang mở, thông báo lỗi và đẩy về trang giỏ hàng
            messages.error(request, "Giỏ hàng của bạn trống!")
            return redirect('cart') 

    # BẮT ĐẦU XỬ LÝ KHI NGƯỜI DÙNG BẤM "XÁC NHẬN ĐẶT HÀNG" (gửi dữ liệu lên qua phương thức POST)
    if request.method == 'POST':
        if order:
            current_time = localtime(now())  # Lấy thời gian hiện tại của hệ thống
            
            # Cập nhật thông tin cho đơn hàng để "chốt đơn"
            order.date_order = current_time  # Ghi nhận thời điểm đặt hàng
            order.complete = True            # Đánh dấu đơn hàng này đã hoàn tất (đóng giỏ hàng)
            order.save()                     # Lưu vào cơ sở dữ liệu

            # Tự động tạo một Hóa đơn (Invoice) để lưu trữ thông tin thanh toán cho đơn hàng này
            invoice = Invoice.objects.create(
                order=order,
                invoice_date=current_time,
                customer=user,
                total_amount=order.get_cart_total # Lấy tổng tiền của đơn hàng
            )
            
            # Hiển thị thông báo thành công cho người dùng kèm theo mã Hóa đơn
            messages.success(
                request,
                f"Đặt hàng thành công! Hóa đơn #{invoice.id} đã được tạo lúc {current_time.strftime('%H:%M:%S, %d-%m-%Y')}"
            )
            # Điều hướng người dùng sang trang xem chi tiết Hóa đơn vừa tạo
            return redirect('invoice_detail', id=invoice.id) 
        else:
            # Đề phòng trường hợp lỗi (gửi form khi không có giỏ hàng)
            messages.error(request, "Không có giỏ hàng để đặt!")
            return redirect('cart')

    # Nếu là yêu cầu xem trang bình thường (GET request), chuẩn bị dữ liệu danh mục sản phẩm
    categories = Category.objects.filter(is_sub=False)

    # Gom tất cả dữ liệu lại vào một dictionary (context) để gửi sang file HTML (app/checkout.html)
    context = {
        'categories': categories,
        'items': items,
        'order': order,
        'cartItems': cartItems,
        'user_not_login': user_not_login,
        'user_login': user_login,
    }
    # Render (Hiển thị) giao diện ra màn hình
    return render(request, 'app/checkout.html', context)


def invoice_detail(request, id):
    # Tìm hóa đơn theo ID, nếu không tồn tại trả về lỗi 404
    invoice = get_object_or_404(Invoice, id=id)
    # Render trang giao diện in Hóa đơn
    return render(request, 'app/invoice_detail.html', {'invoice': invoice})


def order_history(request):
    if request.user.is_authenticated:
        user = request.user
        # Lấy tất cả các đơn hàng đã hoàn tất, sắp xếp từ mới nhất đến cũ nhất
        orders = Order.objects.filter(customer=user, complete=True).order_by('-date_order')
        categories = Category.objects.filter(is_sub=False)
        user_not_login = "hidden"
        user_login = "show"
    else:
        # Bắt buộc đăng nhập
        messages.warning(request, "Bạn cần đăng nhập để xem lịch sử đơn hàng!")
        return redirect('login')

    # Liên kết hóa đơn tương ứng cho từng đơn hàng (dùng để hiển thị link/nút bấm)
    for order in orders:
        try:
            # Gắn biến thuộc tính invoice trực tiếp vào object order
            order.invoice = order.invoice 
        except Invoice.DoesNotExist:
            order.invoice = None # Gắn Null nếu đơn đó không có hóa đơn

    context = {
        'orders': orders,
        'categories': categories,
        'user_not_login': user_not_login,
        'user_login': user_login,
    }
    return render(request, 'app/order_history.html', context)


# ==============================================================================
# 5. THANH TOÁN QUA STRIPE (STRIPE PAYMENTS)
# ==============================================================================

def create_checkout_session(request):
    # Lấy giỏ hàng đang mở của người dùng hiện tại
    order = Order.objects.get(
        customer=request.user,
        complete=False
    )

    # Lấy tổng tiền đơn hàng. Dùng hàm min() để đảm bảo tổng tiền không vượt quá mức tối đa (99999999) nhằm tránh lỗi hệ thống
    total_price = min(int(order.get_cart_total), 99999999)

    # Gọi API của Stripe để tạo một "Phiên thanh toán" (Checkout Session)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'], # Chỉ chấp nhận phương thức thanh toán bằng thẻ
        line_items=[{
            'price_data': {
                'currency': 'vnd',     # Thiết lập tiền tệ là Việt Nam Đồng
                'product_data': {
                    'name': 'Thanh toán đơn hàng' # Tên hiển thị trên màn hình thanh toán của Stripe
                },
                'unit_amount': total_price, # Số tiền cần thanh toán
            },
            'quantity': 1, # Số lượng (mặc định là 1 lần thanh toán cho cả tổng đơn)
        }],
        mode='payment', # Chế độ thanh toán 1 lần (không phải trả góp/đăng ký)
        
        # Nếu khách hàng quẹt thẻ thành công, Stripe sẽ tự động chuyển hướng họ về URL này
        success_url='http://127.0.0.1:8000/success/',
        
        # Nếu khách hàng đang ở trang Stripe nhưng bấm nút "Quay lại" hoặc hủy, họ sẽ về URL này
        cancel_url='http://127.0.0.1:8000/payment/',
    )

    # Chuyển hướng trình duyệt của khách hàng từ web của bạn sang trang thanh toán bảo mật của Stripe
    return redirect(session.url)


def payment(request):
    # Đây là trang trung gian hiển thị tổng tiền trước khi người dùng bấm nút qua Stripe
    
    # Bắt buộc người dùng phải đăng nhập mới được vào trang này
    if request.user.is_authenticated:
        # Tìm đơn hàng đang mở. Hàm get_or_create trả về 1 tuple (object, created_boolean)
        # Nếu chưa có đơn hàng nào đang mở, nó sẽ tự tạo một cái mới.
        order, created = Order.objects.get_or_create(
            customer=request.user,
            complete=False
        )
        context = {
            'order': order
        }
        # Hiển thị file payment.html
        return render(request, 'app/payment.html', context)
    else:
        # Nếu chưa đăng nhập, đá về trang login
        return redirect('login')


def success(request):
    # Đây là trang đích được gọi tới sau khi khách hàng đã thanh toán thành công trên Stripe
    
    # Tìm lại đơn hàng đang mở của vị khách hàng đó
    order = Order.objects.get(customer=request.user, complete=False)

    # Xử lý cập nhật trạng thái "Chốt đơn"
    order.complete = True            # Đóng đơn hàng (không cho thêm bớt sản phẩm nữa)
    order.status = 'approved'        # Đổi trạng thái thành "Đã được phê duyệt"
    order.transaction_id = "stripe_payment"  # Lưu tạm mã giao dịch báo hiệu đây là đơn trả qua Stripe
    order.save()                     # Lưu cập nhật vào Database

    # Hiển thị giao diện báo thành công cho khách hàng
    return render(request, 'app/success.html')

# ==============================================================================
# 6. REST API (Dành cho Mobile, React, Vue, tích hợp bên thứ ba,...)
# API trả về dữ liệu định dạng JSON bằng Django REST Framework (DRF)
# ==============================================================================

## Endpoint GET - Lấy danh sách toàn bộ sản phẩm
@api_view(['GET'])
def get_products(request):
    products = Product.objects.all() # Lấy dữ liệu
    # Chuyển đổi dữ liệu QuerySet thành JSON
    serializer = ProductSerializer(products, many=True) 
    return Response(serializer.data)


## Endpoint POST - Tạo một sản phẩm mới
@api_view(['POST'])
def create_product(request):
    # Nhận dữ liệu JSON gửi lên
    serializer = ProductSerializer(data=request.data)
    
    # Kiểm tra tính hợp lệ
    if serializer.is_valid():
        serializer.save() # Lưu vào database
        return Response(serializer.data, status=201) # 201: Created
        
    # Trả về lỗi nếu dữ liệu thiếu hoặc sai
    return Response(serializer.errors, status=400) # 400: Bad Request


## Endpoint DELETE - Xóa sản phẩm theo ID (pk: primary key)
@api_view(['DELETE'])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk) # Tìm, không có trả về 404
    product.delete() # Lệnh xóa
    return Response({"message": "Product deleted successfully"})


## Endpoint GET - Lấy chi tiết một sản phẩm theo ID
@api_view(['GET'])
def get_product(request, pk):
    product = get_object_or_404(Product, id=pk) # Tìm theo ID
    # Chuyển đổi một đối tượng thành JSON
    serializer = ProductSerializer(product) 
    return Response(serializer.data)