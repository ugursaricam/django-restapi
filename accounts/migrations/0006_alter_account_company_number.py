# Generated by Django 5.0.6 on 2024-07-13 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_alter_account_company_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="company_number",
            field=models.CharField(blank=True, max_length=4),
        ),
    ]