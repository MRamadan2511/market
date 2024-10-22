from .models import Category

def categories_processor(request):
    return {
        'category_list': Category.objects.all()
    }

