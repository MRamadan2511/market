from django.urls import path,include
from . import views



urlpatterns = [

    path('', views.order_list, name='orders_list'),
    path('place_order/', views.place_order, name='place_order'),
    path('detail/<int:order_id>/', views.order_detail, name='order_detail'),
    

]

