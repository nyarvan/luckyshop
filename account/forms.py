from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'name@email.com'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Введіть пароль повторно'
    }))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if len(password) < 8:
            self.add_error('password1', 'Пароль повинен вміщати більше 8 символів')
        if password.isdigit() or password.isalpha():
            self.add_error('password1', 'Пароль повинен складатися з цифр та букв')
        if password != password2:
            self.add_error('password2', 'Паролі не співпадають')


class UserLoginForm(AuthenticationForm):

    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'name@email.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
