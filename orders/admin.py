from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

# 1. ORDER ITEM INLINE (Isay register NAHI karte)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    # Dropdown search ke liye (Products mein search_fields hona lazmi hai)
    autocomplete_fields = ['product'] 
    # Jo fields nazar aayengi
    fields = ['product', 'quantity', 'price']

# 2. MAIN ORDER ADMIN (Sirf isay register karte hain)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'created_at', 
        'payment_status', 
        'colored_total'
    ]

    list_filter = ['is_paid', 'created_at']
    search_fields = ['id']
    ordering = ['-created_at']
    
    # Inline ko yahan shamil karte hain
    inlines = [OrderItemInline]

    # 💰 TOTAL WITH COLOR (SAFE FORMATTING)
    def colored_total(self, obj):
        # Model ki property se total uthayein
        total_val = obj.total_cost
        # Number format karein (comma aur decimal ke saath)
        formatted_price = "{:,.2f}".format(total_val)
        return format_html(
            '<b style="color:#22c55e;">Rs {}</b>',
            formatted_price
        )
    colored_total.short_description = "Total Amount"

    # 💳 PAYMENT STATUS BADGE
    def payment_status(self, obj):
        if obj.is_paid:
            return format_html(
                '<span style="background:#22c55e;color:white;padding:5px 12px;border-radius:20px;font-weight:bold;">{}</span>',
                "Paid"
            )
        return format_html(
            '<span style="background:#ef4444;color:white;padding:5px 12px;border-radius:20px;font-weight:bold;">{}</span>',
            "Unpaid"
        )
    payment_status.short_description = "Status"