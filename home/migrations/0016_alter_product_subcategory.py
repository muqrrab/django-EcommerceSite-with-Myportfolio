# Generated by Django 4.0.4 on 2022-05-30 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.CharField(max_length=6),
        ),
    ]
