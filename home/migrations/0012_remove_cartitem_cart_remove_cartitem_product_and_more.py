# Generated by Django 4.0.3 on 2022-05-27 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_shippingaddress_email_shippingaddress_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
