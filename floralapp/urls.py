from django.urls import path
from floralapp.views import HomeView, ProductView, CollectionView, CheckoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<product_id>/', ProductView.as_view(), name='product'),
    path('collections/<collection_id>/', CollectionView.as_view(), name='collection'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
]