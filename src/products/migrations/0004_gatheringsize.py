# Generated by Django 5.1.4 on 2024-12-13 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='GatheringSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Gathering Size')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified At')),
            ],
            options={
                'verbose_name': 'GatheringSize',
                'verbose_name_plural': 'GatheringSizes',
            },
        ),
    ]