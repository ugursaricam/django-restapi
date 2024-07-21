# Generated by Django 5.0.6 on 2024-07-10 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_account_company_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="company_number",
            field=models.CharField(blank=True, max_length=4, unique=True),
        ),
        migrations.AlterField(
            model_name="account",
            name="phone_number",
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
