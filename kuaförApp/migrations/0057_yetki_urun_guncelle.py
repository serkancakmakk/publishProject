# Generated by Django 5.0.4 on 2024-04-27 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0056_yetki_firma_sil'),
    ]

    operations = [
        migrations.AddField(
            model_name='yetki',
            name='urun_guncelle',
            field=models.BooleanField(default=False),
        ),
    ]
