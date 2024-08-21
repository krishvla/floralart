from django.contrib import admin
from floralapp.models import Category, SubCategory, Product, ProductImage


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)
    empty_value_display = '-empty-'


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('fk_category', 'name', 'description')
    search_fields = ('fk_category__name', 'name', 'description')
    list_filter = ('fk_category__name','name')
    empty_value_display = '-empty-'
    autocomplete_fields = ['fk_category']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    show_change_link = True
    list_display = ('image', 'fk_product', 'fk_product__sku', 'active')
    search_fields = ('fk_product__name', 'fk_product__sku', 'active')
    autocomplete_fields = ['fk_product']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('fk_subcategory', 'name', 'price', 'sku')
    search_fields = ('fk_subcategory__name', 'name', 'price', 'image', 'sku')
    list_filter = ('fk_subcategory__name',)
    empty_value_display = '-empty-'
    autocomplete_fields = ['fk_subcategory']
    inlines = [ProductImageInline]


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'fk_product', 'fk_product__sku', 'active')
    search_fields = ('fk_product__name', 'fk_product__sku', 'active')
    list_filter = ('fk_product__name', 'fk_product__sku', 'active')
    empty_value_display = '-empty-'
    autocomplete_fields = ['fk_product']


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
