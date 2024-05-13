# Generated by Django 5.0.4 on 2024-04-24 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0033_alter_firmauser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='firmauser',
            options={'permissions': (('firma_ekle', 'Firma Ekle'), ('firmalari_listele', 'Firmaları Listele'), ('firma_düzenle', 'Firma Düzenle'), ('tanimlari_listele', 'Tanımları Listele'), ('kullanicilari_listele', 'Kullanıcıları Listele'), ('ürünleri_listele', 'Ürünleri Listele'), ('konumlari_listele', 'Konumları Listele'), ('masalari_listele', 'Masaları Listele'), ('kategorileri_listele', 'Kategorileri Listele'), ('kullanici_ekle', 'Kullanıcı Ekle'), ('ürün_ekle', 'Ürün Ekle'), ('konum_ekle', 'Konum Ekle'), ('masa_ekle', 'Masa Ekle'), ('kategori_ekle', 'Kategori Ekle'), ('kullanici_kayit', 'Kullanıcı Kayıt'), ('ürünleri_gör', 'Ürünleri Gör'))},
        ),
    ]
