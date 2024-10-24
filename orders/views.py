from django.shortcuts import render, redirect
from .models import Order, OrderItem
from carts.cart import Cart

def place_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Create a new Order instance
        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            total_price=cart.get_total_cost()
        )

        # Add the cart items to the order
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['productprofile'],
                price=item['productprofile'].price,
                quantity=item['quantity']
            )

        # Clear the cart after successful order placement
        cart.clear()

        # Redirect to a confirmation page or show a success message
        return render(request, 'orders/confirmation.html', {'order': order})

    return redirect('checkout')
