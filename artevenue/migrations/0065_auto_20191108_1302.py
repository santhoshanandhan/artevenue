# Generated by Django 2.2.4 on 2019-11-08 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artevenue', '0064_auto_20191108_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='original_art_original_art_category',
            name='stock_image_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='original_art_category', to='artevenue.Stock_image_category'),
        ),
        migrations.AlterField(
            model_name='payment_details',
            name='payment_txn_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
