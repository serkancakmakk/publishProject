# Generated by Django 5.0.4 on 2024-05-10 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0077_alter_siparis_siparis_durum'),
    ]

    operations = [
        migrations.AddField(
            model_name='yetki',
            name='kullanici_güncelle',
            field=models.BooleanField(default=False),
        ),
    ]
