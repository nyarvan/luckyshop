from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

from cart.cart import Cart
from .models import Category, Catalog, TypeClothes, Product, OtherImageProduct


def pagination(request, products):
    paginator = Paginator(sort_products(request, products), 9)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def sort_products(request, products):
    sort = str(request.GET.get('sort', ''))
    if sort:
        return products.order_by(sort)
    return products


def filter_products(request, *args, **kwargs):
    size = []
    color = []
    filter_param = dict()
    for key, value in request.GET.items():
        if key == 'min_price':
            filter_param['price__gte'] = value
        elif key == 'max_price':
            filter_param['price__lte'] = value
        elif 'size_shoes' in key:
            id_size = key.replace('size_shoes-', '')
            size.append(int(id_size))
        elif 'size_cloth' in key:
            id_size = key.replace('size_cloth-', '')
            size.append(int(id_size))
        elif 'color' in key:
            id_color = key.replace('color-', '')
            color.append(int(id_color))

    if len(size) > 0:
        filter_param['size__id__in'] = size
    if len(color) > 0:
        filter_param['color__id__in'] = color

    return Product.objects.filter(*args, **filter_param, **kwargs).distinct()


def get_path(request):
    path = {'default': request.path}
    for key, value in request.GET.items():
        if key not in ('sort', 'page'):
            path[key] = value
    return path


@method_decorator(require_GET, name='dispatch')
class HomepageView(ListView):
    template_name = 'homepage.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.select_related('type').order_by('?')[:4]

    def get_context_data(self, *, object_list=None, **kwargs):
        path = get_path(self.request)
        cart = Cart(self.request)

        context = super().get_context_data(**kwargs)
        type_cloth = TypeClothes.objects.distinct().select_related('catalog').order_by('?')[:8]
        context['type'] = type_cloth
        context['path'] = path
        context['cart'] = cart
        return context


@method_decorator(require_GET, name='dispatch')
class SearchProductsView(ListView):
    template_name = 'products.html'
    context_object_name = 'products'

    def get_result_search(self):
        return str(self.request.GET.get('result', '')).title().strip()

    def get_queryset(self):
        search = self.get_result_search()
        return filter_products(self.request, Q(full_name__contains=search) | Q(name__contains=search) |
                               Q(type__full_name__contains=search) | Q(catalog__full_name__contains=search))

    def get_context_data(self, *, object_list=None, **kwargs):
        search = self.get_result_search()
        title = f'Результат поиска - {search}'
        path = get_path(self.request)
        cart = Cart(self.request)

        context = super().get_context_data(**kwargs)
        context['page_obj'] = pagination(self.request, self.get_queryset())
        context['title'] = title
        context['path'] = path
        context['cart'] = cart
        return context


@method_decorator(require_GET, name='dispatch')
class ProductsListView(ListView):
    template_name = 'products.html'
    context_object_name = 'products'
    special = None
    new_in = None

    def get_queryset(self):
        filter_attrs = dict()
        if self.special:
            filter_attrs['special'] = self.special
        if self.new_in:
            filter_attrs['new_in'] = self.new_in

        for key, value in self.kwargs.items():
            if key == 'slug_category':
                filter_attrs['category__slug'] = value
            elif key == 'slug_catalog':
                filter_attrs['catalog__slug'] = value
            elif key == 'slug_type_clothes':
                filter_attrs['type__slug'] = value

        return filter_products(self.request, **filter_attrs)

    def get_context_data(self, *, object_list=None, **kwargs):
        path = get_path(self.request)
        elements_title = []
        for key, value in self.kwargs.items():
            if key == 'slug_category':
                category = get_object_or_404(Category, slug=value)
                elements_title.append(category.full_name)
            elif key == 'slug_catalog':
                catalog = get_object_or_404(Catalog, slug=value)
                elements_title.append(catalog.full_name)
            elif key == 'slug_type_clothes':
                type_clothes = get_object_or_404(TypeClothes, slug=value)
                elements_title.append(type_clothes.full_name)

        if self.special:
            elements_title.append('Скидки')
        if self.new_in:
            elements_title.append('Новинки')

        title = ' - '.join(elements_title)
        cart = Cart(self.request)

        context = super().get_context_data(**kwargs)
        context['page_obj'] = pagination(self.request, self.get_queryset())
        context['path'] = path
        context['title'] = title
        context['cart'] = cart
        return context


@method_decorator(require_GET, name='dispatch')
class ProductDetailView(DetailView):
    template_name = 'product.html'
    context_object_name = 'product'
    model = Product
    slug_url_kwarg = 'slug_product'
    queryset = Product.objects.all().select_related('type')

    def get_context_data(self, **kwargs):
        product = self.get_object()
        products_be_like = Product.objects.exclude(id=product.id).filter(category=product.category)[:8]
        other_images_product = OtherImageProduct.objects.filter(product=product)
        cart = Cart(self.request)

        context = super().get_context_data(**kwargs)
        context['products_be_like'] = products_be_like
        context['other_images'] = other_images_product
        context['cart'] = cart
        return context
