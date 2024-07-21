from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account

# Create your models here.

class Product(models.Model):
    product_number          = models.CharField(max_length=4, unique=True)
    product_name            = models.CharField(max_length=200, unique=True)
    slug                    = models.SlugField(max_length=200, unique=True)
    price                   = models.IntegerField(blank=True)
    images                  = models.ImageField(upload_to='photos/products', blank=True)
    stock                   = models.IntegerField(blank=True)
    is_available            = models.BooleanField(default=True)
    category                = models.ForeignKey(Category, on_delete = models.CASCADE)
    create_date             = models.DateTimeField(auto_now_add=True)
    modified_date           = models.DateTimeField(auto_now = True)
    allowed_users           = models.ManyToManyField(Account, blank=True, related_name='allowed_products')

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name
