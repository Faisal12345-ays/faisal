from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid
from decimal import Decimal


# 📁 CATEGORY MODEL
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# 📦 PRODUCT MODEL
class Product(models.Model):

    UNIT_CHOICES = [
        ('1kg', '1 kg'),
        ('500g', '500Grams'),
        ('50g', '50 Grams'),
        ('250g', '250Grams'),
        ('5kg', '5killograms'),
        ('piece', 'Piece'),
        ('cup', 'Cup'),
        ('glass', 'Glass'),
        ('1 Unit','1 Unit'),
         ('220 ml','220 ML'),
    ]

    name = models.CharField(max_length=200)
    product_id = models.CharField(max_length=10, unique=True, blank=True)
    slug = models.SlugField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='products'
    )
     # products/models.py mein Product class ke andar:
    brand = models.CharField(max_length=100, default="Instacart")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)

    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='piece')

    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        blank=True
    )

    # 🔥 DESCRIPTION FIELD
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Product features like weight, brand, etc."
    )

    expiry_days = models.IntegerField(default=0)
    expiry_date = models.DateField(blank=True, null=True)

    image = models.ImageField(
        upload_to='products/',
        default='products/default.jpg',
        blank=True
    )

    suggestions = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False
    )

    # 🔹 STRING
    def __str__(self):
        return self.name

    # 🔹 AUTO SAVE
    def save(self, *args, **kwargs):
        if not self.product_id or self.product_id == "":
            self.product_id = str(uuid.uuid4())[:8].upper()

        if self.expiry_days > 0:
            self.expiry_date = timezone.now().date() + timedelta(days=self.expiry_days)

        super().save(*args, **kwargs)

    # 🔹 EXPIRED
    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False

    # 🔹 NEAR EXPIRY
    @property
    def is_near_expiry(self):
        if self.expiry_date:
            today = timezone.now().date()
            return today <= self.expiry_date <= (today + timedelta(days=7))
        return False

    # 🔹 STOCK
    @property
    def stock_status(self):
        return "In Stock" if self.quantity > 0 else "Out of Stock"

    # 🔹 DISCOUNT PRICE
    @property
    def get_discounted_price(self):
        if self.discount > 0:
            reduction = (Decimal(self.discount) / Decimal(100)) * Decimal(self.price)
            return Decimal(self.price) - reduction
        return Decimal(self.price)

    # 🔹 HAS DISCOUNT
    @property
    def has_discount(self):
        return self.discount > 0


# 🖼️ PRODUCT GALLERY (NEW MODEL)
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = models.ImageField(
        upload_to='products/gallery/'
    )

    def __str__(self):
        return f"Image for {self.product.name}"