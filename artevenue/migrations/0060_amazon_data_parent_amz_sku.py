# Generated by Django 2.2.4 on 2019-10-21 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artevenue', '0059_remove_amazon_data_parent_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazon_data',
            name='parent_amz_sku',
            field=models.CharField(default='', max_length=15, null=True),
        ),
    ]
