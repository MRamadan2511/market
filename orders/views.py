from django.shortcuts import render, redirect, get_object_or_404
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

    # return redirect('checkout')



def order_list(request):
    customer = request.user
    order_list = Order.objects.filter(customer=customer)

    context = {
        'order_list': order_list,
    }

    return render(request, 'orders/orders_list.html', context)



def order_detail(request, order_id):
    
    order = get_object_or_404(Order, pk=order_id)
    
    statuses = [
        'New', 
        'Accepted on Market', 
        'Picked', 
        'In Route', 
        'Delivered'
    ]

    # Failure statuses
    failure_statuses = ['Canceled', 'Failed', 'Delayed']
    print(order.status)
    # Find current status position
    current_status = order.status.status # Assuming 'status' is a field in Order model
    if current_status in statuses:
        print(order.status)
        status_index = statuses.index(current_status)
        progress_percentage = (status_index + 1) * (100 // len(statuses))
    else:
        progress_percentage = 100 if current_status in failure_statuses else 0


    context = {
        'order': order,
        'current_status': current_status,
        'progress_percentage': progress_percentage,
        'failure_statuses': failure_statuses,
    }

    return render(request, 'orders/order_detail.html', context)