from django.contrib import admin
from .models import *
from django.utils.timezone import localtime, now
from .models import ChatHistory

# ── ChatHistory ──────────────────────────────────────
@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_message', 'bot_reply', 'timestamp')
    search_fields = ('user_message', 'bot_reply', 'user_id')
    list_filter = ('timestamp',)


# ── ProductVariant inline (hiện trong trang Product) ─
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 3          # Số dòng trống mặc định khi thêm mới
    fields = ('color', 'color_hex', 'size', 'stock')


# ── Product ──────────────────────────────────────────
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'digital')
    inlines = [ProductVariantInline]   # ← Thêm variant ngay trong Product


# ── Order ────────────────────────────────────────────
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'get_local_date_order',
                    'get_local_approved_date', 'complete', 'transaction_id', 'status')
    list_filter = ('complete', 'status', 'date_order')
    search_fields = ('customer__username', 'transaction_id')
    actions = ['approve_orders', 'reject_orders']

    def get_local_date_order(self, obj):
        return localtime(obj.date_order).strftime('%d-%m-%Y %H:%M:%S')
    get_local_date_order.short_description = 'Thời gian đặt hàng'

    def get_local_approved_date(self, obj):
        if obj.approved_date:
            return localtime(obj.approved_date).strftime('%d-%m-%Y %H:%M:%S')
        return "Chưa duyệt"
    get_local_approved_date.short_description = 'Thời gian duyệt'

    @admin.action(description='Duyệt các đơn hàng đã chọn')
    def approve_orders(self, request, queryset):
        updated = queryset.update(status='approved', approved_date=now())
        self.message_user(request, f'{updated} đơn hàng đã được duyệt.')

    @admin.action(description='Từ chối các đơn hàng đã chọn')
    def reject_orders(self, request, queryset):
        updated = queryset.update(status='canceled', approved_date=None)
        self.message_user(request, f'{updated} đơn hàng đã bị từ chối.')


# ── OrderItem ────────────────────────────────────────
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'get_local_date_added')

    def get_local_date_added(self, obj):
        return localtime(obj.date_added).strftime('%d-%m-%Y %H:%M:%S')
    get_local_date_added.short_description = 'Thời gian thêm vào'


# ── Các model còn lại ────────────────────────────────
admin.site.register(Category)
admin.site.register(ShippingAddress)
admin.site.register(ProductVariant)
