# Generated by Django 5.0.4 on 2024-04-24 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0054_remove_yetki_ürünleri_gör'),
    ]

    operations = [
        migrations.AddField(
            model_name='yetki',
            name='kullanicilari_listele',
            field=models.BooleanField(default=False),
        ),
    ]
