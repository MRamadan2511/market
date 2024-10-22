from django.shortcuts import render
from django.views.generic import DetailView

from .models import ProductProfile, Category, Product, Market


def products(request):
    products_list = Product.objects.all()
    categories = Category.objects.all()
    product_profile= ProductProfile.objects.all()

    context = {
        'products_list': products_list,
        'categories': categories,
        'product_profile': product_profile,
        }
    
    return render(request, 'products/shop.html', context)


def markets_list(request):
    market_list= Market.objects.all()

    context = {
        'market_list': market_list,
        }
    
    return render(request, 'products/maket_list.html', context)



def category_view(request):
    category_list= Category.objects.all()

    context = {
        'category_list': category_list,
        }   
    
    return render(request, 'products/category_list.html', context)






def category_view(request, slug):
    category = Category.objects.get(slug=slug)  # Get the category based on the slug
    products = Product.objects.filter(category=category)  # Filter products by the selected category
    product_profiles = ProductProfile.objects.filter(product__in=products)  
    categories = Category.objects.all()

    context = {
        'category': category,
        'products': products,  # Include products in the context
        'product_profiles': product_profiles,  # Include products in the context
        'categories': categories,  
    }

    return render(request, 'products/category_detail.html', context)