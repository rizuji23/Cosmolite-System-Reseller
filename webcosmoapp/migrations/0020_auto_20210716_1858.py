# Generated by Django 3.2.4 on 2021-07-16 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webcosmoapp', '0019_rename_keluarahan_alamat_kelurahan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alamat',
            name='kecamatan',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='alamat',
            name='kelurahan',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='alamat',
            name='kotakab',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='alamat',
            name='provinsi',
            field=models.TextField(),
        ),
    ]