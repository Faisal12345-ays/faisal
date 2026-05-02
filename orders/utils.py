# orders/utils.py
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import Order  # ok to import models

def send_bill_email(order):
    """Send invoice email to customer"""
    if order.customer_email:  # check email exists
        subject = f"Your InstaCart Invoice #{order.id}"
        message = render_to_string('orders/email_invoice.html', {'order': order})
        email = EmailMessage(subject, message, to=[order.customer_email])
        email.content_subtype = "html"
        email.send()