# Generated by Django 5.0.6 on 2024-07-10 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_account_company_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="company_number",
            field=models.CharField(blank=True, max_length=4),
        ),
    ]
