# Generated by Django 4.0.3 on 2022-05-16 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_product_image_product_imageback_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='longdescription',
            field=models.TextField(blank=True, max_length=5000),
        ),
        migrations.AddField(
            model_name='product',
            name='shortdescription',
            field=models.TextField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='imageback',
            field=models.ImageField(blank=True, upload_to='product/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='imagefront',
            field=models.ImageField(blank=True, upload_to='product/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='imageother1',
            field=models.ImageField(blank=True, upload_to='product/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='imageother2',
            field=models.ImageField(blank=True, upload_to='product/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]