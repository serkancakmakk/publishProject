# Generated by Django 5.0.3 on 2024-04-04 19:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("kuaförApp", "0007_masa_masa_qr_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="masa",
            name="masa_qr_code",
        ),
    ]
