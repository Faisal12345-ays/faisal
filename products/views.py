from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# ✅ 1. HOME PAGE (Product List Grouped by Category)
@login_required
# products/views.py

def product_list(request):
    query = request.GET.get('q')
    cat_id = request.GET.get('category')
    
    # 1. Categories ko unke products ke saath mangwayein (Related Name Fix)
    categories = Category.objects.all().prefetch_related('products')

    # 2. Agar Search ho rahi hai
    if query:
        from django.db.models import Q
        categories = categories.filter(
            Q(products__name__icontains=query) | Q(products__product_id__icontains=query)
        ).distinct()
    
    # 3. 🔥 CATEGORY FILTER LOGIC (THE FIX)
    # Jab aap kisi circle par click karenge, ye sirf us category ko filter karega
    if cat_id:
        categories = categories.filter(id=cat_id)

    return render(request, 'products/list.html', {
        'categories': categories,
        'query': query
    })


# ✅ 2. PRODUCT DETAIL PAGE
def product_detail(request, product_id):
    # product_id string wali ID hai (maslan ABC0001)
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'products/detail.html', {'product': product})

# ✅ 3. SIGNUP VIEW (Actual Logic Added)
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to InstaCart, {user.username}!")
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'products/signup.html', {'form': form})


# ✅ 4. USER PROFILE VIEW
@login_required
def profile_view(request):
    # User ke apne saare orders nikaalein
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'products/profile.html', {'orders': orders})


# ✅ 5. ORDER HISTORY (User Dashboard)
@login_required
def order_history(request):
    # 🚨 FIXED: Yahan bhi function ke andar import karein
    from orders.models import Order
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/dashboard.html', {'orders': orders})


# ✅ 6. SEARCH SUGGESTIONS (AJAX)
def search_suggestions(request):
    query = request.GET.get('q', '')
    data = []
    if len(query) > 1:
        prods = Product.objects.filter(
            Q(name__icontains=query) | Q(product_id__icontains=query)
        )[:8]
        for p in prods:
            data.append({
                'name': p.name, 
                'price': float(p.get_discounted_price), 
                'url': f"/product/{p.product_id}/"
            })
    return JsonResponse({'data': data})