# Generated by Django 2.2.4 on 2019-10-05 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artevenue', '0056_auto_20191005_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice_date',
            field=models.DateTimeField(null=True),
        ),
    ]
