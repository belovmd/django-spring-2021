# Generated by Django 3.2.2 on 2021-05-26 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0003_auto_20210526_2117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='birth',
            new_name='birthday',
        ),
    ]
