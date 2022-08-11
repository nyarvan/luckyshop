from django import forms
from .models import Order


class CreateOrderForm(forms.ModelForm):
    DELIVERY_METHOD = [
        ('Самовывоз', 'Самовивозом'),
        ('Доставка', 'Доставкою'),
        ('Новой почтой', 'Доставка Новою почтою')
    ]

    PAYMENT_METHOD = [
        ('Наличными', 'Оплата готівкою'),
        ('Картой', 'Оплата картою'),
        ('Наложенный платеж', 'Накладеним платежем')
    ]

    delivery = forms.ChoiceField(choices=DELIVERY_METHOD, widget=forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }))

    payment = forms.ChoiceField(choices=PAYMENT_METHOD, widget=forms.RadioSelect(attrs={
                'class': 'form-check-input'}))

    class Meta:
        model = Order
        exclude = ['created', 'updated', 'paid']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '+38(066) 123 45 67'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'you@example.com'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
