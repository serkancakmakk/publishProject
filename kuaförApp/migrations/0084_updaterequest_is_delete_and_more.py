# Generated by Django 5.0.4 on 2024-05-13 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0083_yetki_konum_güncelle'),
    ]

    operations = [
        migrations.AddField(
            model_name='updaterequest',
            name='is_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='updaterequest',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
