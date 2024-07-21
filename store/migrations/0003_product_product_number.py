# Generated by Django 5.0.6 on 2024-07-08 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_product_allowed_users"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="product_number",
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]