# Generated by Django 4.2 on 2025-06-08 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forecast',
            old_name='name',
            new_name='city',
        ),
    ]
