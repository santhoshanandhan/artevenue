# Generated by Django 2.2.4 on 2019-11-26 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artevenue', '0072_auto_20191126_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='original_art',
            name='artist',
            field=models.CharField(max_length=600, null=True),
        ),
    ]
