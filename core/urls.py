from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # ✅ MUST ADD THIS
    path('', include('products.urls')),
    path('orders/', include('orders.urls')),
]