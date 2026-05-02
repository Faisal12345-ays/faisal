from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Category
from orders.models import Order, OrderItem
from django.db.models import Count
from datetime import date
import json
from django.db.models import Sum

# 🔥 TOP SELLING PRODUCTS
top_products = (
    OrderItem.objects
    .values('product__name')
    .annotate(total_sold=Sum('quantity'))
    .order_by('-total_sold')[:5]
)

top_labels = [p['product__name'] for p in top_products]
top_data = [p['total_sold'] for p in top_products]

# 🛒 ADD TO CART
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    order, created = Order.objects.get_or_create(id=1)

    item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity

    item.save()

    return redirect('cart_detail')


# 📊 DASHBOARD
def dashboard(request):

    categories = Category.objects.all()
    cat_labels = []
    cat_data = []

    for c in categories:
        count = Product.objects.filter(category=c).count()
        cat_labels.append(c.name)
        cat_data.append(count)

    # Expiry data
    expired = Product.objects.filter(expiry_date__lt=date.today()).count()
    valid = Product.objects.filter(expiry_date__gte=date.today()).count()

    # Unit distribution
    units = Product.objects.values('unit').annotate(count=Count('id'))
    unit_labels = [u['unit'] for u in units]
    unit_data = [u['count'] for u in units]

    # JSON convert (VERY IMPORTANT)
    context = {
    'cat_labels': json.dumps(cat_labels),
    'cat_data': json.dumps(cat_data),
    'expiry_data': json.dumps([expired, valid]),
    'unit_labels': json.dumps(unit_labels),
    'unit_data': json.dumps(unit_data),

    # 🔥 YAHAN ADD KARNA HAI
    'top_labels': json.dumps(top_labels),
    'top_data': json.dumps(top_data),
}

    return render(request, 'dashboard.html', context)