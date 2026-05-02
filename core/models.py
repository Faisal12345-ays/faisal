from django.db import models
from products.models import Product


def total_price(self):
        return self.product.price * self.quantity