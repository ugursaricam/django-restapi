from django.shortcuts import render, redirect
from django.http import HttpResponse
from carts.models import CartItem
from .models import Order, OrderProduct, Payment
import datetime
import json
from store.models import Product
from django.contrib import messages
from django.db import transaction
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


import csv
import os
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # Kullanıcının sepetteki ürünlerini al
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    # Toplam ve vergi hesaplama
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax
    
    if request.method == 'POST':
        # Kullanıcı bilgilerini request.user nesnesinden çek
        data = Order()
        data.user = current_user
        data.first_name = current_user.first_name
        data.last_name = current_user.last_name
        data.company_name = current_user.company_name
        data.company_number = current_user.company_number
        data.phone = current_user.phone_number
        data.email = current_user.email
        data.order_note = request.POST.get('order_note', '')
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        
        # Sipariş numarası oluştur
        yr = int(datetime.date.today().strftime('%Y'))
        mt = int(datetime.date.today().strftime('%m'))
        dt = int(datetime.date.today().strftime('%d'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()
        
        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
        context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,
        }

        for item in cart_items:
            order_product = OrderProduct()
            order_product.order_id = order.id
            order_product.user_id = current_user.id
            order_product.product_id = item.product_id
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.ordered = True
            order_product.save()

            # Ürün stoktan düşürme
            # product = Product.objects.get(id=item.product_id)
            # product.stock -= item.quantity
            # product.save()

        # Sepeti temizle
        order.is_ordered = True
        order.save()
        CartItem.objects.filter(user=current_user).delete()

        # Send order received email to customer
        user = current_user
        mail_subject = 'Thank you for your order!'
        message = render_to_string('orders/order_received_email.html', {
            'user': user,
            'order': order,
        })
        to_email1 = current_user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email1])
        send_email.send()

        return render(request, 'orders/order_complete.html', context)

    else:
        return redirect('home')
    

def is_admin(user):
    return user.is_admin

@user_passes_test(is_admin)
def create_csv_view(request):
    if request.method == 'POST':
        now = timezone.now()
        current_datetime = now.strftime("%Y%m%d%H%M%S")  # YYYYMMDDHHMMSS formatında datetime
        filename = f"{current_datetime}.csv"

        # CSV dosyasını bellekte oluşturma
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        csvwriter = csv.writer(response, delimiter=';')

        company_names = set()
        order_products = OrderProduct.objects.filter(order__csv_exported=False)

        # Çarpma işlemi yapılacak ürünlerin product_number değerleri (örnek olarak)
        products_to_multiply = {
            '0024': 3,  # Product_number '0001' olan ürünün quantity'si 2 ile çarpılacak
            '0025': 2,  # Product_number '0002' olan ürünün quantity'si 3 ile çarpılacak
            # Diğer ürün product_number değerleri ve çarpılacak değerler
        }
        
        for order_product in order_products:
            # Quantity'yi çarpma işlemi
            quantity = order_product.quantity
            product_number = order_product.product.product_number  # Ürünün product_number'ı
            if product_number in products_to_multiply:
                quantity *= products_to_multiply[product_number]

            csvwriter.writerow([
                order_product.order.company_number,  # customer_number
                product_number,                      # product_number
                quantity,                            # Çarpılmış quantity değeri
                now.strftime('%Y%m%d')               # datetime (YYYYMMDD formatında)
            ])
            company_names.add(order_product.order.company_name)

            # Siparişin CSV'ye aktarıldığını işaretle
            order_product.order.csv_exported = True
            order_product.order.save()

        company_names_list = list(company_names)
        return response

    return render(request, 'orders/create_csv.html')

