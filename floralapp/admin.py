from django.contrib import admin
from django.utils.html import format_html

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
    list_display = ('fk_subcategory', 'name', 'price', 'sku', 'image_preview')
    readonly_fields = ('image_preview',)
    search_fields = ('fk_subcategory__name', 'name', 'price', 'image', 'sku')
    list_filter = ('fk_subcategory__name',)
    empty_value_display = '-empty-'
    autocomplete_fields = ['fk_subcategory']
    inlines = [ProductImageInline]

    def image_preview(self, obj):
        if obj.product_image:
            return format_html(
                '<img src="{}" width="100" />',
                obj.product_image.url
            )
        return "No Image"

    image_preview.short_description = "Image Preview"


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('fk_product', 'fk_product__sku', 'active', 'image_preview')
    search_fields = ('fk_product__name', 'fk_product__sku', 'active')
    list_filter = ('fk_product__name', 'fk_product__sku', 'active')
    empty_value_display = '-empty-'
    autocomplete_fields = ['fk_product']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" />', obj.image.url)
        return "-"


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
