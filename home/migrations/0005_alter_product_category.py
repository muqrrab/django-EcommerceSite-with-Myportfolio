# Generated by Django 4.0.3 on 2022-05-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_product_description_product_longdescription_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('clothing', 'Clothing'), ('shoes', 'Shoes')], default='clothing', max_length=8),
        ),
    ]
