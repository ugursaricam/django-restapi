from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('create_csv/', views.create_csv_view, name='create_csv'),
]   