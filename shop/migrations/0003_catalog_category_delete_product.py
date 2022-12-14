# Generated by Django 4.0.3 on 2022-03-27 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50)),
                ('full_name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('position', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to='images/category')),
                ('test', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ('position',),
                'index_together': {('slug',)},
            },
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
