# Generated by Django 5.0.4 on 2024-05-13 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0086_delete_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='firma',
            name='price_in_use',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='urun',
            name='urun_fiyat',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
