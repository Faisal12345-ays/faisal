from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ye sahi jagah hai include karne ki
    path('', include('products.urls')),   # Home page (products)
    path('cart/', include('orders.urls')), # Cart aur Orders
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'images/logo.png')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)