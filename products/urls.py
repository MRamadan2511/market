from django.urls import path,include
from . import views



urlpatterns = [
    path('', views.products, name='products'),
    path('markets_list', views.markets_list, name='markets_list'),
    path('category_list', views.category_view, name='category_list'),
    path('category_detail/<slug:slug>/', views.category_view, name='category_detail'),
    

]