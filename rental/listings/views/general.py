from django.shortcuts import render
from listings.models import Review

def home(request):
    reviews = Review.objects.select_related('user').order_by('created_at')[:3]
    return render(request, 'listings/home.html', {'page_obj': reviews})

def about(request):
    return render(request, 'listings/about-us.html')

def privacy(request):
    return render(request, 'listings/privacy-policy.html')
