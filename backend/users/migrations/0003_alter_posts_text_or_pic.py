# Generated by Django 4.0 on 2022-06-09 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_users_code_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='text_or_pic',
            field=models.BooleanField(default=False),
        ),
    ]