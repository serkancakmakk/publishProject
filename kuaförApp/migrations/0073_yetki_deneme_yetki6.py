# Generated by Django 5.0.4 on 2024-05-01 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0072_remove_yetki_deneme_yetki6'),
    ]

    operations = [
        migrations.AddField(
            model_name='yetki',
            name='deneme_yetki6',
            field=models.BooleanField(default=False),
        ),
    ]
