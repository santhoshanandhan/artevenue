# Generated by Django 2.2.4 on 2019-08-12 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artevenue', '0042_auto_20190812_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homelane_data',
            name='acrylic',
            field=models.CharField(default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='homelane_data',
            name='board',
            field=models.CharField(default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='homelane_data',
            name='mount',
            field=models.CharField(default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='homelane_data',
            name='print_medium',
            field=models.CharField(default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='homelane_data',
            name='stretch',
            field=models.CharField(default='', max_length=15, null=True),
        ),
    ]
