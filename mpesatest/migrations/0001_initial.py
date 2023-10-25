# Generated by Django 4.2.6 on 2023-10-24 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCallback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MerchantRequestID', models.CharField(max_length=255)),
                ('CheckoutRequestID', models.CharField(max_length=255)),
                ('ResponseCode', models.CharField(max_length=10)),
                ('ResponseDescription', models.CharField(max_length=255)),
                ('CustomerMessage', models.TextField()),
            ],
        ),
    ]
