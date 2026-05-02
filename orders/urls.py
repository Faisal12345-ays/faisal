from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),  # /cart/

    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('short-add/', views.add_by_short_id, name='add_by_short_id'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.dashboard, name='order_history'),
    path('shipping-details/', views.checkout_details, name='checkout_details'),
    path('payment/', views.payment_selection, name='payment_selection'),
    path('my-orders/', views.order_history, name='order_history'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('admin-stats/', views.admin_stats, name='admin_stats'),
]