# Generated by Django 5.0.4 on 2024-05-01 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0069_yetki_deneme_yetki4'),
    ]

    operations = [
        migrations.AddField(
            model_name='yetki',
            name='deneme_yetki5',
            field=models.BooleanField(default=False),
        ),
    ]
