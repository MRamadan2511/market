from django.db import models
from orders.models import Order
from products.models import ProductProfile
import uuid
from accounts.models import User




# class Cart(models.Model):
#     id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     user = models.ForeignKey(User,  on_delete=models.CASCADE)
#     completed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    

    
#     def __str__(self):
#         return str(self.id)
    
#     @property
#     def total_price(self):
#         cartitems = self.cartitems.all()
#         total = sum([item.price for item in cartitems])
#         return total
    
    
      
#     @property
#     def num_of_items(self):
#         cartitems = self.cartitems.all()
#         quantity = sum([item.quantity for item in cartitems])
#         return quantity



# class CartItem(models.Model):
#     product = models.ForeignKey(ProductProfile, on_delete=models.CASCADE, related_name='items')
#     cart = models.ForeignKey(Cart, on_delete= models.CASCADE, related_name="cartitems")
#     quantity = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return self.product.market_name
    
#     @property
#     def price(self):
#         new_price = self.product.price * self.quantity
#         return new_price