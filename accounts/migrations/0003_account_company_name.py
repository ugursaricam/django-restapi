# Generated by Django 5.0.6 on 2024-06-26 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_userprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="company_name",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
