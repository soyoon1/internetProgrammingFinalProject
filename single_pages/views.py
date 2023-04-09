from django.shortcuts import render
from mall.models import Item, Manufacturer,Category
from django.db.models import Q

# Create your views here.
def landing(request):
    recent_items = Item.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html', {
        'recent_items': recent_items,
    })

def about_us(request):
    manufacturer = Manufacturer.objects.all()
    item = Item.objects.all()
    category = Category.objects.all()
    #category_item = [["Category"], ["개수"], ]
    #for category in Category.objects.all():
    #    category_item.append(["category.name", category.item_set.count])
    return render(request, 'single_pages/about_us.html', {
        'manufacturer': manufacturer,
        'item': item,
    #    'category_item': category_item,
        'category': category,
    })