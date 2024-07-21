from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True, allowed_users=request.user).order_by('product_name')
        paginator = Paginator(products, 60)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True, allowed_users=request.user).order_by('product_name')
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        product_count = products.count()

    # Sepetteki ürünleri kontrol et
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
    cart_item_product_ids = [item.product.id for item in cart_items]

    context = {
        'products': paged_product,
        'cart_items': cart_items,
        'cart_item_product_ids': cart_item_product_ids,
        'product_count' : product_count,
    }
    return render(request, 'store/store.html', context)



def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = None
    product_count = 0
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-create_date').filter(product_name__icontains=keyword)
            product_count = products.count()

    context = {
        'products': products,
        'product_count':product_count,
    }
    return render(request, 'store/store.html', context)


