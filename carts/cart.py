from django.conf import settings

from products.models import ProductProfile

class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['productprofile'] = ProductProfile.objects.get(pk=p)
            # print(self.cart[str(p)]['productprofile'])
        for item in self.cart.values():
            productprofile = item['productprofile']

            item['total_price'] = productprofile.price * item['quantity']
            # item['get_display_name'] = productprofile
      

            yield item
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
        
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    def add(self, productprofile_id, quantity=1, update_quantity=False):
        productprofile_id = str(productprofile_id)
        if productprofile_id not in self.cart:
            self.cart[productprofile_id] = {'quantity': 0, 'id': productprofile_id}
        
        if update_quantity:
            self.cart[productprofile_id]['quantity'] = quantity
        else:
            self.cart[productprofile_id]['quantity'] += quantity

        if self.cart[productprofile_id]['quantity'] <= 0:
            self.remove(productprofile_id)

        self.save()
    
    def remove(self, productprofile_id):
        productprofile_id = str(productprofile_id)
        if productprofile_id in self.cart:
            del self.cart[productprofile_id]
            self.save()
            print("okay")
            print(self.cart)  # Debugging
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['productprofile'] = ProductProfile.objects.get(pk=p)

        total_cost = sum(item['productprofile'].price * item['quantity'] for item in self.cart.values())
    
        # Format the total cost with commas and two decimal places
        return "{:,.2f}".format(total_cost)
    
    def get_item(self, productprofile_id):
        if str(productprofile_id) in self.cart:
            return self.cart[str(productprofile_id)]
        else:
            return None