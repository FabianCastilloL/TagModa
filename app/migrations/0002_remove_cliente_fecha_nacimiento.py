# Generated by Django 4.0 on 2022-05-09 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='fecha_nacimiento',
        ),
    ]
