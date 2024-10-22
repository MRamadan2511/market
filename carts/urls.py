from django.urls import path,include
from . import views



urlpatterns = [
    
    path('', views.cart, name='cart'),
    path('cart_bag_update/', views.cart_bag_update, name='cart_bag_update'),
    path('cart_total_cost/', views.cart_total_cost, name='cart_total_cost'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart_remove/<int:productprofile_id>/', views.cart_remove, name="cart_remove"),
    path('update_cart/<int:productprofile_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('cart_bag_count/', views.cart_bag_count, name='cart_bag_count'),
    # path('decrement/<int:productprofile_id>/', views.cart_decrement, name='cart_decrement'),
    # path('remove/<int:productprofile_id>/', views.cart_remove, name='cart_remove'),
    

]

