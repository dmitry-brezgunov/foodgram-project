# Generated by Django 3.1 on 2020-09-08 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_auto_20200908_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Уникальный адрес'),
        ),
    ]
