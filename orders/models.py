from django.db import models
from products.models import Product
from django.contrib.auth.models import User

# 🧾 ORDER MODEL (Pura Bill)
# orders/models.py mein Order class ko aise badlein:

class Order(models.Model):
     STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True)
     is_paid = models.BooleanField(default=False)
     discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # 🔥 YE 3 NAYE FIELDS LAZMI ADD KAREIN
     customer_name = models.CharField(max_length=200, blank=True, null=True)
     customer_phone = models.CharField(max_length=20, blank=True, null=True)
     customer_address = models.TextField(blank=True, null=True)

     def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

    # 💰 PURE BILL KA TOTAL
@property
def total_cost(self):
    items_total = sum(item.total_price for item in self.items.all())
    # 400 RS SHIPPING FEE ADD KAR DI
    final = float(items_total) - float(self.discount) + 300.0 
    return max(final, 0)

def __str__(self):
        return f"Order #{self.id} by {self.user.username if self.user else 'Guest'}"


# 📦 ORDER ITEM MODEL (Har aik product ki line)
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE
    )
    quantity = models.FloatField(default=1.0)
    
    # Woh price jis par item becha gaya
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True, 
        default=0
    )

    # 1. PEHCHAN (Dropdown mein ID aur Name dikhayega)
    def __str__(self):
        # Ab ye dikhayega: ABC000001 - Apple
        if self.product:
            return f"{self.product.product_id} - {self.product.name}"
        return f"Item {self.id}"

    # 2. 💰 EK LINE KA TOTAL (Price x Quantity)
    @property
    def total_price(self):
        if self.price:
            return float(self.price) * float(self.quantity)
        return 0

    # 3. 🔥 AUTO PRICE SAVING (Save hote waqt discounted price khud uthaye)
    def save(self, *args, **kwargs):
        # Agar price manually nahi likhi, toh product ki discounted price uthao
        if (not self.price or self.price == 0) and self.product:
            self.price = self.product.get_discounted_price
        super().save(*args, **kwargs)