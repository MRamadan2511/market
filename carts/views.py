from django.shortcuts import render
from .cart import Cart
from django.http import JsonResponse, HttpResponse
import json
from products.models import ProductProfile

def cart(request):

    return render(request, 'carts/cart.html')


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return render(request, 'carts/cart_bag.html')


def update_cart(request, productprofile_id, action):
    cart = Cart(request)

    if action == 'increment':
        cart.add(productprofile_id, 1, update_quantity=False)
    elif action == 'decrement':
        cart.add(productprofile_id, -1, update_quantity=False)
    
    item = cart.get_item(productprofile_id)
    print(item)
    if item:
        product = ProductProfile.objects.get(pk=productprofile_id)

        context = {
            'item': {
                'productprofile': product,
                # 'market_name':product.market_name,
                'quantity': item['quantity'],
                'total_price': item['quantity'] * product.price,
            }
        }
        
        # Trigger cart count update along with rendering the updated cart item
        response = render(request, 'carts/partials/cart_item.html', context)
        response['HX-Trigger'] = 'update-menu-cart'  # Include the updated cart count
        return response
        
    else:
        # Trigger item removal and cart count update
        response = HttpResponse('')
        response['HX-Trigger'] = 'update-menu-cart'
        return response




def cart_bag_update(request):
    return render(request, "carts/cart_bag.html")

def cart_total_cost(request):
    return render(request, "carts/partials/cart_total.html")


from django.conf import settings


def cart_remove(request, productprofile_id):
    cart = Cart(request)
    cart.remove(productprofile_id)
    # Return an empty response with a trigger for HTMX to remove the item row
    
    response = HttpResponse('')
    
    # Trigger multiple events for updating cart bag and total price
    response['HX-Trigger'] = json.dumps({
        'update-menu-cart': {},  # This event will update the cart bag count
        'update-cart-total': {},  # This event will update the total price in the cart
        'item-removed': {},  # This event will remove the item from the cart
    })
    return response



def cart_bag_count(request):
    cart = Cart(request)
    return HttpResponse(len(cart))  # Return the count of items 


# from django.shortcuts import redirect
# from .cart import Cart

# def cart_increment(request, productprofile_id):
#     cart = Cart(request)
#     cart.add(productprofile_id, quantity=1, update_quantity=False)
#     return redirect('cart')

# def cart_decrement(request, productprofile_id):
#     cart = Cart(request)
#     cart.remove(productprofile_id)
#     return redirect('cart')

# def cart_remove(request, productprofile_id):
#     cart = Cart(request)
#     cart.remove(productprofile_id)
#     return redirect('cart_detail')
