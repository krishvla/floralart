import json
import urllib.parse

from django.shortcuts import render
from django.views.generic import TemplateView
from floralapp.models import Product, SubCategory, ProductImage
from floralapp.utils import categories_list


# Create your views here.

class HomeView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        recent_items = Product.objects.all().order_by('-created_at')[:8]
        most_viewed_items = Product.objects.all().order_by('-view_count')[:5]
        context['nav_floral_data'] = categories_list()
        context['recent_items'] = recent_items
        context['most_viewed_items'] = most_viewed_items
        print(context)
        return render(request, 'home.html', context=context)


class ProductView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        product_id = kwargs['product_id']
        product = Product.objects.get(id=product_id)
        product_images = ProductImage.objects.filter(fk_product=product)
        context['nav_floral_data'] = categories_list()
        context['product'] = product
        context['product_images'] = product_images
        context['c'] = [1,2,3,4]
        return render(request, 'product_detail.html', context=context)


class CollectionView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        collection_id = kwargs.get('collection_id')
        collection = SubCategory.objects.get(id=collection_id)
        collection_items = Product.objects.filter(fk_subcategory=collection).order_by('-created_at')
        context['nav_floral_data'] = categories_list()
        context['collection_items'] = collection_items
        context['collection'] = collection
        return render(request, 'collection.html', context=context)


class CheckoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = {}
        context['nav_floral_data'] = categories_list()
        cart_data = request.COOKIES.get('cart', '')
        decoded_cart_data = urllib.parse.unquote(cart_data)
        try:
            # Attempt to decode JSON data
            cart = json.loads(decoded_cart_data)
        except json.JSONDecodeError:
            # Handle the case where JSON is invalid or empty
            cart = {}

        if cart:
            for product_id, value in cart.items():
                product_obj = Product.objects.get(id=product_id)
                cart[product_id]['product_image'] = product_obj.product_image
                cart[product_id]['max_stock'] = product_obj.max_stock
        context['cart'] = cart
        return render(request, 'checkout.html', context)

