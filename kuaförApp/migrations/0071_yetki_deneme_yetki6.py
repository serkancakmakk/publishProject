# Generated by Django 5.0.4 on 2024-05-01 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0070_yetki_deneme_yetki5'),
    ]

    operations = [
        migrations.AddField(
            model_name='yetki',
            name='deneme_yetki6',
            field=models.BooleanField(default=False),
        ),
    ]
