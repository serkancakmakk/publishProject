# Generated by Django 5.0.4 on 2024-04-20 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuaförApp', '0025_alter_firmauser_user_cinsiyet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmauser',
            name='user_adres',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
