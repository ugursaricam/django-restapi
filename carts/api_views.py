from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem
from .context_processors import counter

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@api_view(['POST'])
def add_to_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    cart_id = _cart_id(request)

    if current_user.is_authenticated:
        is_cart_exists = CartItem.objects.filter(user=current_user, cart__cart_id=_cart_id).exists()
        if is_cart_exists:
            cart = Cart.objects.filter(cart_id=cart_id,user=current_user)
            cart_item, created = CartItem.objects.filter(product=product, user=current_user, cart=cart)
        else:
            cart, created = Cart.objects.get_or_create(cart_id=cart_id,user=current_user)
            cart_item, created = CartItem.objects.get_or_create(product=product, user=current_user, cart=cart)

    cart_item.quantity += 1
    cart_item.save()

    cart_count = counter(request)['cart_count']
    return Response({'cart_count': cart_count, 'product_quantity': cart_item.quantity, 'cart_item_id': cart_item.id}, status=status.HTTP_200_OK)

@api_view(['POST'])
def remove_from_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            cart_count = counter(request)['cart_count']
            return Response({'cart_count': cart_count, 'product_quantity': cart_item.quantity, 'product_id': product_id}, status=status.HTTP_200_OK)
        else:
            cart_item.delete()
            cart_count = counter(request)['cart_count']
            return Response({'cart_count': cart_count, 'product_quantity': 0, 'product_id': product_id}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
        cart_count = counter(request)['cart_count']
        return Response({'cart_count': cart_count, 'product_quantity': 0, 'cart_item_id': cart_item_id, 'product_id': product_id}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)