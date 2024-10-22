from django.db import models
from accounts.models import Customer
from products.models import Product, ProductProfile
from django.db.models import Sum
from django.utils import timezone



class OrderStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status


from django.db import models
from accounts.models import User
from products.models import ProductProfile

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.email}"

    def calculate_total(self):
        """
        Calculate the total amount of the order based on the cart items and their prices.
        """
        total = sum(item.get_subtotal() for item in self.cart_items.all())
        self.total_amount = total
        self.save()
        return total

