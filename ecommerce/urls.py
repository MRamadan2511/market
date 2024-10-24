from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from .  import views

urlpatterns = [
    path('admin/', admin.site.urls),


    #Base URL
    path("", views.home, name='home'),
    path("contact/", views.contact, name='contact'),
    path("page_404/", views.page_404, name='page_404'),


    #Apps URL
    path('products/', include('products.urls')),
    path('cart/', include('carts.urls')),
    path('checkout/', include('billing.urls')),
    path('orders/', include('orders.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)