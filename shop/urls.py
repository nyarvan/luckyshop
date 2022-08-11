from django.urls import path, include
from shop.views import HomepageView, ProductsListView, SearchProductsView, ProductDetailView

app_name = "shop"

shop_urls = [
    path('<slug:slug_category>', ProductsListView.as_view(), name='category_products_view'),
    path('type-clothes/<slug:slug_type_clothes>', ProductsListView.as_view(), name='products_type_clothes_view'),
    path('<slug:slug_category>/special-offer', ProductsListView.as_view(special=True),
         name='products_category_special_view'),
    path('<slug:slug_category>/novelties', ProductsListView.as_view(new_in=True),
         name='novelties_products_category_view'),
    path('<slug:slug_category>/<slug:slug_catalog>', ProductsListView.as_view(),
         name='products_category_catalog_view'),
    path('<slug:slug_category>/<slug:slug_catalog>/special-offer', ProductsListView.as_view(special=True),
         name='products_category_catalog_special_view'),
    path('<slug:slug_category>/<slug:slug_catalog>/<slug:slug_type_clothes>', ProductsListView.as_view(),
         name='products_category_type_clothes_view'),
]

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),

    path('search', SearchProductsView.as_view(), name='search_product'),
    path('special-offer', ProductsListView.as_view(special=True), name='special_products_view'),
    path('novelties', ProductsListView.as_view(new_in=True), name='novelties_products_view'),
    path('shop/', include(shop_urls)),
    path('product/<slug:slug_product>', ProductDetailView.as_view(), name='product')
]
