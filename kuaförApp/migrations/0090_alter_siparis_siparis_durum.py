# Generated by Django 5.0.4 on 2024-05-15 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0089_rename_error_errorreport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siparis',
            name='siparis_durum',
            field=models.IntegerField(choices=[(1, 'Bekleyen'), (2, 'Hazırlandı'), (3, 'Tamamlandı'), (8, 'İptal Edilip Silindi'), (9, 'İptal Edildi')], default=0),
        ),
    ]
