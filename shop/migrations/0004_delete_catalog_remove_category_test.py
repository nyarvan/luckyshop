# Generated by Django 4.0.3 on 2022-03-27 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_catalog_category_delete_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Catalog',
        ),
        migrations.RemoveField(
            model_name='category',
            name='test',
        ),
    ]