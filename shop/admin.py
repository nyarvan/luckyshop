from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Catalog, TypeClothes, Product, Size, Color, OtherImageProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_name', 'slug', 'position', 'image']
    list_editable = ['full_name', 'slug', 'position', 'image']
    list_display_links = ['name', ]
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ['name', 'full_name', 'slug']
    list_editable = ['full_name', 'slug']
    list_display_links = ['name', ]
    prepopulated_fields = {'slug': ('name', )}


@admin.register(TypeClothes)
class TypeClothesAdmin(admin.ModelAdmin):
    list_display = ['name', 'catalog', 'full_name', 'slug', 'image']
    list_filter = ['catalog', ]
    list_editable = ['full_name', 'slug', 'image']
    list_display_links = ['name', ]
    prepopulated_fields = {'slug': ('name', )}


class OtherImagesProductAdmin(admin.TabularInline):
    model = OtherImageProduct
    raw_id_fields = ['product']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'catalog', 'type', 'price', 'available', 'special', 'new_in', 'old_price']
    list_filter = ['category', 'catalog', 'type', 'available', 'special', 'new_in']
    list_editable = ['price', 'available', 'special', 'new_in', 'old_price']
    list_display_links = ['name', ]
    search_fields = ['name', 'full_name', ]
    prepopulated_fields = {'slug': ('name', )}
    fields = ['full_name', 'name', 'slug', 'image', 'view_image', 'category', 'catalog', 'type', 'price', 'special',
              'old_price', 'size', 'color', 'description', 'detail', 'info', 'available', 'new_in']
    readonly_fields = ['view_image']
    inlines = [OtherImagesProductAdmin]

    def view_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150">')

    view_image.short_description = 'Фотография'


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['catalog', 'name']
    list_filter = ['catalog', ]
    list_editable = ['name', ]


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', ]
