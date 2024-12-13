# Generated by Django 5.1.4 on 2024-12-13 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Coupon Code')),
                ('discount_percentage', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Discount Percentage')),
                ('max_discount_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Maximum Discount Amount')),
                ('valid_from', models.DateTimeField(verbose_name='Valid From')),
                ('valid_to', models.DateTimeField(verbose_name='Valid To')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
            ],
        ),
    ]