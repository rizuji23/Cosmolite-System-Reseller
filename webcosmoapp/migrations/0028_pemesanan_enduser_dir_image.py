# Generated by Django 3.2 on 2021-07-29 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcosmoapp', '0027_auto_20210728_2324'),
    ]

    operations = [
        migrations.AddField(
            model_name='pemesanan_enduser',
            name='dir_image',
            field=models.FileField(null=True, upload_to='buktipembayaranenduser'),
        ),
    ]
