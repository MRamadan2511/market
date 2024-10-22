from django.contrib import admin
from .models import Market,Category,Brand,ProductUnit,PackingUnit,Product,ProductProfile

admin.site.register(Market)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductUnit)
admin.site.register(PackingUnit)
# admin.site.register(Product)
# admin.site.register(ProductProfile)


class ProductProfileAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_at', 'updated_at',  # Make these fields read-only
    )
admin.site.register(ProductProfile, ProductProfileAdmin)




class ProductAdmin(admin.ModelAdmin):
    readonly_fields = (
        'created_at', 'updated_at',  # Make these fields read-only
    )
admin.site.register(Product, ProductAdmin)