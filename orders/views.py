from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product, Category
from .models import Order, OrderItem
from datetime import datetime
import json
from django.db.models import Sum

# ✅ 1. CART DETAIL (Display Items + Smart Suggestions)
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    grand_total = 0
    suggested_products = Product.objects.none()

    # Cart mein mojud products ki IDs
    product_ids_in_cart = list(cart.keys())

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            price = product.get_discounted_price
            total_price = float(price) * float(quantity)
            grand_total += total_price

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'total_price': total_price
            })

            # 🔥 Smart Suggestions
            suggested_products |= product.suggestions.exclude(id__in=product_ids_in_cart)

        except Product.DoesNotExist:
            continue

    # 🔥 SHIPPING FEE LOGIC
    shipping_fee = 0
    if grand_total > 0:
        shipping_fee = 300.0
        grand_total += shipping_fee

    context = {
        'cart_items': cart_items,
        'grand_total': grand_total,
        'shipping_fee': shipping_fee,  # 🔥 template ke liye
        'suggestions': suggested_products.distinct()[:3]
    }

    return render(request, 'orders/cart.html', context)


# ✅ 2. ADD TO CART
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Expiry Check
    if product.is_expired:
        messages.error(request, f"❌ Sorry, {product.name} is expired and cannot be added.")
        return redirect('product_list')

    cart = request.session.get('cart', {})
    qty = int(request.POST.get('quantity', 1))

    # Add or Update quantity
    cart[str(product_id)] = cart.get(str(product_id), 0) + qty
    request.session['cart'] = cart
    
    messages.success(request, f"✅ {product.name} added to cart!")
    return redirect('cart_detail')


# ✅ 3. ADD BY SHORT CODE (e.g., '001')
def add_by_short_id(request):
    if request.method == "POST":
        short_id = request.POST.get('short_id', '').strip()
        
        # Excel wali product_id ke aakhir se match karega
        product = Product.objects.filter(product_id__endswith=short_id).first()

        if not product:
            messages.error(request, "❌ Product not found with this code!")
        elif product.is_expired:
            messages.error(request, "❌ This product has expired!")
        else:
            cart = request.session.get('cart', {})
            cart[str(product.id)] = cart.get(str(product.id), 0) + 1
            request.session['cart'] = cart
            messages.success(request, f"✅ {product.name} added via code!")
            
    return redirect('cart_detail')


# ✅ 4. REMOVE FROM CART
def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session.modified = True
        messages.info(request, "Item removed from your cart.")
    return redirect('cart_detail')


# ✅ 5. STEP 1: SHIPPING DETAILS
@login_required
# orders/views.py

@login_required
def checkout_details(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('product_list')
        
    if request.method == "POST":
        # 1. Form se data pakrein
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # 2. 'shipping_info' naam ke dibbe mein save karein
        request.session['shipping_info'] = {
            'name': name,
            'phone': phone,
            'address': address,
        }
        # Django ko batayein ke session badal gaya hai
        request.session.modified = True
        
        return redirect('payment_selection')
        
    return render(request, 'orders/checkout_details.html')

@login_required
def payment_selection(request):
    # Check karein ke kya pichle page se address aaya?
    if 'shipping_info' not in request.session:
        messages.error(request, "Please enter your address first.")
        return redirect('checkout_details')
    return render(request, 'orders/payment.html')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    shipping = request.session.get('shipping_info')

    # Agar data nahi hai toh wapas bhejain (Yahan se error aa raha tha)
    if not cart or not shipping:
        messages.error(request, "Session missing. Please enter details again.")
        return redirect('checkout_details')

    # Order create karein
    order = Order.objects.create(
        user=request.user,
        customer_name=shipping['name'],
        customer_phone=shipping['phone'],
        customer_address=shipping['address']
    )

    for p_id, qty in cart.items():
        p = Product.objects.get(id=p_id)
        OrderItem.objects.create(
            order=order, product=p, quantity=qty, price=p.get_discounted_price
        )

    # Order ke baad kachra saaf karein
    request.session['cart'] = {}
    request.session.pop('shipping_info', None)
    
    return redirect('order_success', order_id=order.id)
@login_required

def order_detail(request, order_id):
    # Order dhoondein jo sirf isi user ka ho
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

# ✅ 8. SUCCESS PAGE
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})


# ✅ 9. ORDER HISTORY (User Dashboard)
# orders/views.py

@login_required
def order_history(request):
    # 🔒 PRIVACY FIX: Sirf usi bande ke orders dhoondein jo login hai
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/dashboard.html', {'orders': orders})

def order_detail(request, order_id):
    # 🔒 PRIVACY FIX: Agar koi URL mein kisi aur ki ID likhe toh woh na khule
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


# ✅ 10. GENERATE INVOICE (Printable Bill)
# orders/views.py mein is function ko update karein

def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # 1. Items ka asli total nikaalein
    items_subtotal = sum(float(item.total_price) for item in order.items.all())
    
    # 2. Shipping fee set karein
    shipping_fee = 400.0
    
    # 3. Grand total (Subtotal + Shipping)
    grand_total = items_subtotal + shipping_fee
    
    return render(request, 'orders/invoice.html', {
        'order': order,
        'subtotal': items_subtotal,
        'shipping_fee': shipping_fee,
        'grand_total': grand_total,
    })

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'orders/dashboard.html', {
        'orders': orders
    })

@login_required
def checkout_final(request):
    cart = request.session.get('cart', {})
    # Session se wahi 'ship_info' mangwayein
    info = request.session.get('ship_info')

    if not cart or not info:
        # Agar data nahi mila toh wapas bhejain (Yahi error aapko aa raha tha)
        messages.error(request, "Session expired. Please enter details again.")
        return redirect('checkout_details')

    # Naya Order create karein
    order = Order.objects.create(
        user=request.user,
        customer_name=info['name'],
        customer_phone=info['phone'],
        customer_address=info['address']
    )

    for p_id, qty in cart.items():
        p = Product.objects.get(id=p_id)
        OrderItem.objects.create(
            order=order, 
            product=p, 
            quantity=qty, 
            price=p.get_discounted_price
        )

    # Order ke baad memory saaf karein
    request.session['cart'] = {}
    request.session['ship_info'] = {}
    
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def admin_stats(request):
    if not request.user.is_staff:
        return redirect('product_list')

    total_revenue = Order.objects.filter(is_paid=True).aggregate(total=Sum('items__price'))['total'] or 0
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    out_of_stock = Product.objects.filter(quantity=0).count()

    return render(request, 'orders/admin_stats.html', {
        'revenue': total_revenue,
        'orders_count': total_orders,
        'pending': pending_orders,
        'stock_issue': out_of_stock
    })