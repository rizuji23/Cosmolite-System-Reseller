# Generated by Django 3.2 on 2021-07-28 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcosmoapp', '0026_pemesanan_pengirimanid'),
    ]

    operations = [
        migrations.AddField(
            model_name='pemesanan_enduser',
            name='alamat',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pemesanan_enduser',
            name='nama_enduser',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pemesanan_enduser',
            name='pembayaran',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pemesanan_enduser',
            name='pengiriman',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
