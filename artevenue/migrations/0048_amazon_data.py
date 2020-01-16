# Generated by Django 2.2.4 on 2019-08-23 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artevenue', '0047_homelane_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amazon_data',
            fields=[
                ('amazon_key', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(default='', max_length=128, null=True)),
                ('description', models.CharField(blank=True, default='', max_length=2000)),
                ('part_number', models.CharField(max_length=30, null=True)),
                ('category_name', models.CharField(default='', max_length=128, null=True)),
                ('is_published', models.BooleanField(default=False)),
                ('aspect_ratio', models.DecimalField(decimal_places=18, max_digits=21, null=True)),
                ('image_type', models.CharField(max_length=1, null=True)),
                ('orientation', models.CharField(max_length=20, null=True)),
                ('max_width', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('max_height', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('min_width', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('publisher', models.CharField(max_length=600, null=True)),
                ('artist', models.CharField(max_length=600, null=True)),
                ('colors', models.CharField(max_length=600, null=True)),
                ('key_words', models.CharField(max_length=2000, null=True)),
                ('url', models.CharField(blank=True, default='', max_length=1000)),
                ('thumbnail_url', models.CharField(blank=True, default='', max_length=1000)),
                ('framed_url', models.CharField(blank=True, default='', max_length=1000)),
                ('framed_thumbnail_url', models.CharField(blank=True, default='', max_length=1000)),
                ('promotion_name', models.CharField(default='', max_length=128, null=True)),
                ('quantity', models.IntegerField()),
                ('item_unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_sub_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_disc_amt', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('moulding_name', models.CharField(default='', max_length=30, null=True)),
                ('moulding_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('print_medium_name', models.CharField(default='', max_length=30, null=True)),
                ('print_medium_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('mount_name', models.CharField(default='', max_length=30, null=True)),
                ('mount_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('board_name', models.CharField(default='', max_length=30, null=True)),
                ('board_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('acrylic_name', models.CharField(default='', max_length=30, null=True)),
                ('acrylic_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('stretch_name', models.CharField(default='', max_length=30, null=True)),
                ('stretch_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('image_width', models.DecimalField(decimal_places=0, max_digits=3)),
                ('image_height', models.DecimalField(decimal_places=0, max_digits=3)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('ordered', models.BooleanField(default=False)),
                ('order_number', models.CharField(blank=True, default='', max_length=15)),
                ('order_date', models.DateField(blank=True, null=True)),
                ('acrylic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Acrylic')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Board')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='artevenue.Stock_image_category')),
                ('moulding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Moulding')),
                ('mount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Mount')),
                ('print_medium', models.ForeignKey(default='PAPER', on_delete=django.db.models.deletion.PROTECT, to='artevenue.Print_medium')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.Stock_image')),
                ('product_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='artevenue.Product_type')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Promotion')),
                ('stretch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Stretch')),
            ],
        ),
    ]
