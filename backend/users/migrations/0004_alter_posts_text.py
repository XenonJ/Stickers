# Generated by Django 4.0 on 2022-06-09 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_posts_text_or_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='text',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
