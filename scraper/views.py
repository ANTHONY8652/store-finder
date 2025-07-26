from django.shortcuts import render
from .models import Product
from django.utils import timezone
from datetime import timedelta
from django.core.management import call_command


def product_list(request):
    query = request.GET.get('q')
    products = []
    if query:
        term = query.lower()
        cutoff = timezone.now() - timedelta(hours=12)
        recent = Product.objects.filter(search_term=term, last_updated__gte=cutoff)

        if recent.exists():
            products = recent
        
        else:
            call_command('scrape_sites', search_term=term)
            products = Product.objects.filter(search_term=term)
    
    else:
        products = Product.objects.all().order_by('-last_updated')[:20]
    
    return render(request, 'scraper/products.html', {
        'products': products,
        'search_term': query or '',
    })

# Create your views here.
