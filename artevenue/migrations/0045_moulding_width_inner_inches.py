# Generated by Django 2.2.4 on 2019-08-19 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artevenue', '0044_auto_20190812_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='moulding',
            name='width_inner_inches',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
    ]
