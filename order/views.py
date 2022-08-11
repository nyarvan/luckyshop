from django.shortcuts import render
from .forms import CreateOrderForm
from .models import OrderItem
from cart.cart import Cart


def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=int(item['price']),
                                         size=str(item['size']), count=item['count'])
            cart.clear()
            return render(request, 'created.html', {'order': order})
    form = CreateOrderForm()
    return render(request, 'checkout.html', {
        'form': form,
        'cart': cart,
    })
