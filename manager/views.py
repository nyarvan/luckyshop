from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from order.models import Order
from django.core.paginator import Paginator
from django.views.generic import ListView


def is_manager(user):
    return user.groups.filter(name='manager').exists()


@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(user_passes_test(is_manager), name='dispatch')
class OrderListView(ListView):
    template_name = 'order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(paid=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        paginator = Paginator(self.get_queryset(), 9)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj
        return context


@login_required(login_url='/login/')
@user_passes_test(is_manager)
def close_order_view(request, order_pk):
    Order.objects.filter(pk=order_pk).update(paid=False)
    return redirect('manager:orders')
