from django.shortcuts import render



def home(request):

    return render(request, 'home.html')



def contact(request):

    return render(request, 'contact.html')


def page_404(request):

    return render(request, '404.html')