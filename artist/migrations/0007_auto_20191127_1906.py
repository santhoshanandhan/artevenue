# Generated by Django 2.2.4 on 2019-11-27 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0006_auto_20191127_1831'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artist',
            old_name='zip',
            new_name='pin_code',
        ),
    ]
