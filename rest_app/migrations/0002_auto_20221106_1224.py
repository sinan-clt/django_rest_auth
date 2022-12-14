# Generated by Django 3.2.15 on 2022-11-06 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('quantity', models.IntegerField()),
                ('product_image', models.ImageField(blank=True, upload_to='photos/products')),
                ('is_available', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'django_product',
            },
        ),
        migrations.AlterModelTable(
            name='user',
            table='django_user',
        ),
    ]
