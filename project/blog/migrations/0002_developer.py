# Generated by Django 4.1.3 on 2022-12-14 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=40, verbose_name='Имя разработчика')),
                ('job', models.CharField(max_length=30, verbose_name='Профессия')),
                ('bio', models.TextField(verbose_name='О себе')),
            ],
            options={
                'verbose_name': 'Разработчик',
                'verbose_name_plural': 'Разработчики',
            },
        ),
    ]
