# Generated by Django 5.0.3 on 2024-04-06 14:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kuaförApp", "0010_shorturl_url_shorturl_url_qr_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="masa",
            name="masa_short_url",
            field=models.CharField(blank=True, null=True, unique=True),
        ),
    ]
