from django.shortcuts import render
from django.views import generic

# Create your views here.
def home_page(request):
    return render(request, 'treadweb/index.html')
