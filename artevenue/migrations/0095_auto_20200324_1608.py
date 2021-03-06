# Generated by Django 2.2.4 on 2020-03-24 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artevenue', '0094_auto_20200324_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collage_stock_image',
            fields=[
                ('collage_id', models.AutoField(primary_key=True, serialize=False)),
                ('stock_image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Stock_image')),
                ('stock_image_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='artevenue.Stock_image_category')),
            ],
        ),
        migrations.AddField(
            model_name='stock_collage',
            name='set_of',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='Collage_product_stock_image',
        ),
    ]
