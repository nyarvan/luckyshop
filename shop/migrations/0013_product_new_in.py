# Generated by Django 4.0.3 on 2022-03-27 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_product_catalog'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='new_in',
            field=models.BooleanField(default=True),
        ),
    ]
