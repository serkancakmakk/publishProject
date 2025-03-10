# Generated by Django 5.0.3 on 2024-04-11 21:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("kuaförApp", "0017_alter_firmauser_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="firmauser",
            options={
                "permissions": (
                    ("kullanicilari_listele", "Kullanıcıları Listele"),
                    ("ürünleri_listele", "Ürünleri Listele"),
                    ("katlari_listele", "Katları Listele"),
                    ("masalari_listele", "Masaları Listele"),
                    ("kategorileri_listele", "Kategorileri Listele"),
                    ("kullanici_kayit", "Kullanıcı Kayıt"),
                    ("ürünleri_gör", "Ürünleri Gör"),
                )
            },
        ),
    ]
