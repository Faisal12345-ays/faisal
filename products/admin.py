from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from datetime import timedelta
from .models import Category, Product

# --- IMPORT/EXPORT LIBRARIES ---
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin

# 🎨 Admin Header
admin.site.site_header = "My Smart Inventory System 🚀"
admin.site.site_title = "InstaCart Admin"
admin.site.index_title = "Welcome to Mr Faisal 👋"

# 📁 CATEGORY ADMIN
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# 📦 PRODUCT RESOURCE (Excel Import Logic)
class ProductResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'id')
    )

    class Meta:
        model = Product
        fields = ('name', 'product_id', 'category', 'price', 'unit', 'discount', 'expiry_days')
        import_id_fields = ('product_id',) 
        exclude = ('image',) 

    def before_import(self, dataset, **kwargs):
        new_headers = []
        for header in dataset.headers:
            if header:
                clean_header = str(header).lower().strip()
                new_headers.append(clean_header)
            else:
                new_headers.append(header)
        dataset.headers = new_headers

# 📦 PRODUCT ADMIN
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    
    list_display = [
        'product_id',
        'name',
        'category',
        'colored_price',
        'status_badge',
        'expiry_alert_badge',
        'near_expiry_badge',
        'stock_badge',
    ]
    class Media:
        css = {
            'all': ('css/admin_custom.css',)
        }
        
    search_fields = ['name', 'product_id']
    list_filter = ['category']
    ordering = ['-id']
    raw_id_fields = ('suggestions',)

    # 💰 Price Decoration (FIXED)
    def colored_price(self, obj):
        return format_html('<b style="color:#2563eb;">Rs {}</b>', obj.price)
    colored_price.short_description = "Price"

    # 📦 Status Badge (FIXED: Added {} and argument)
    def status_badge(self, obj):
        if obj.expiry_date:
            today = timezone.now().date()
            if obj.expiry_date < today:
                return format_html('<span style="background:#ef4444;color:white;padding:5px 12px;border-radius:20px;">{}</span>', "Expired")
            elif obj.expiry_date <= today + timedelta(days=3):
                return format_html('<span style="background:#f59e0b;color:white;padding:5px 12px;border-radius:20px;">{}</span>', "Near Expiry")
            else:
                return format_html('<span style="background:#22c55e;color:white;padding:5px 12px;border-radius:20px;">{}</span>', "Fresh")
        return "-"
    status_badge.short_description = "Status"

    # ⚠ Expiry Alert (FIXED: Added {} and argument)
    def expiry_alert_badge(self, obj):
        if obj.expiry_date:
            days = (obj.expiry_date - timezone.now().date()).days
            if days <= 0: 
                return "Expired"
            elif days <= 3:
                return format_html('<span style="color:#f59e0b;font-weight:bold;">⚠ {} days left</span>', days)
            return format_html('<span style="color:#22c55e;">{} days left</span>', days)
        return "N/A"
    expiry_alert_badge.short_description = "Expiry Alert"

    # ⏳ Near Expiry Badge (FIXED: Added {} and argument)
    def near_expiry_badge(self, obj):
        if obj.expiry_date:
            days = (obj.expiry_date - timezone.now().date()).days
            if 0 <= days <= 3:
                return format_html('<span style="background:#f59e0b;color:white;padding:4px 10px;border-radius:12px;">{}</span>', "YES")
        return format_html('<span style="background:#e5e7eb;color:black;padding:4px 10px;border-radius:12px;">{}</span>', "NO")
    near_expiry_badge.short_description = "Near Expiry"

    # 📦 Stock Badge (FIXED: Added {} and argument)
    def stock_badge(self, obj):
        if obj.quantity > 0: 
            return format_html('<span style="background:#22c55e;color:white;padding:5px 12px;border-radius:20px;">{}</span>', "In Stock")
        return format_html('<span style="background:#ef4444;color:white;padding:5px 12px;border-radius:20px;">{}</span>', "Out of Stock")
    stock_badge.short_description = "Stock"

    # 📊 Top Summary Data
    def changelist_view(self, request, extra_context=None):
        products = Product.objects.all()
        # Safe calculation to avoid recursion
        expired_count = sum(1 for p in products if p.expiry_date and p.expiry_date < timezone.now().date())
        
        extra_context = extra_context or {}
        extra_context['summary_data'] = {
            'total': products.count(),
            'expired': expired_count,
            'near_expiry': sum(1 for p in products if p.expiry_date and 0 <= (p.expiry_date - timezone.now().date()).days <= 3),
            'in_stock': sum(1 for p in products if p.quantity > 0),
        }
        return super().changelist_view(request, extra_context=extra_context)