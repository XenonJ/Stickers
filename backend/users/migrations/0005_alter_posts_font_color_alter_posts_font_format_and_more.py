# Generated by Django 4.0 on 2022-06-09 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_posts_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='font_color',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='font_format',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='font_size',
            field=models.CharField(max_length=500, null=True),
        ),
    ]