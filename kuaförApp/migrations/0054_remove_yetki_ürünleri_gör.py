# Generated by Django 5.0.4 on 2024-04-24 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0053_yetki_kategori_ekle_yetki_kategorileri_listele_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yetki',
            name='ürünleri_gör',
        ),
    ]
