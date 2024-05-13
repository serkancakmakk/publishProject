# Generated by Django 5.0.4 on 2024-04-24 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('kuaförApp', '0039_alter_firmauser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmauser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
