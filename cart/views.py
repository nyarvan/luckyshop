from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from shop.models import Product
from django.views.decorators.http import require_GET


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart.html', {'cart': cart})


@require_GET
def cart_add(request, product_id):
    size = request.GET.get('size')
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, size, 1, False)
    if request.GET.get('add_cart'):
        return redirect('shop:category_products_view', slug_category=product.category.slug)
    elif request.GET.get('add_to_buy'):
        return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')
