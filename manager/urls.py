from django.urls import path
from .views import OrderListView, close_order_view

app_name = 'manager'

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/update/<int:order_pk>', close_order_view, name='close_order')
]
