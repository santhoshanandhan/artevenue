# Generated by Django 2.2.4 on 2020-09-25 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallerywalls', '0007_auto_20200924_1934'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery_item',
            name='product_name',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]
