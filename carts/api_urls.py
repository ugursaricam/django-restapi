from django.urls import path
from . import api_views  # API görünümlerini içe aktarın

urlpatterns = [
    path('cart/add/<int:product_id>/', api_views.add_to_cart, name='add_to_cart_api'),
    path('cart/remove/<int:product_id>/<int:cart_item_id>/', api_views.remove_from_cart, name='remove_from_cart_api'),
    path('cart/remove_item/<int:product_id>/<int:cart_item_id>/', api_views.remove_cart_item, name='remove_cart_item_api'),
    path('cart/update_quantity/<int:product_id>/<int:cart_item_id>/', api_views.update_quantity, name='update_quantity_api'),

]
