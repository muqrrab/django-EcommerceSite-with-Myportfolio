# Generated by Django 4.0.3 on 2022-05-16 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_product_category_alter_product_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.CharField(choices=[('women', 'Women'), ('men', 'Men')], default='women', max_length=100),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=5)),
                ('name', models.ManyToManyField(to='home.product')),
            ],
        ),
    ]
