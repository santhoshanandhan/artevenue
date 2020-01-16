# Generated by Django 2.2.4 on 2019-09-23 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artevenue', '0051_auto_20190917_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice_items_view',
            fields=[
                ('invoice_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('item_unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_sub_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_disc_amt', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('moulding_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('print_medium_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('mount_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('board_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('acrylic_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('stretch_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('image_width', models.DecimalField(decimal_places=0, max_digits=3)),
                ('image_height', models.DecimalField(decimal_places=0, max_digits=3)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'invoice_items_view',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_id', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_number', models.CharField(blank=True, default='', max_length=15)),
                ('invoice_date', models.DateField(blank=True, null=True)),
                ('session_id', models.CharField(blank=True, default='', max_length=40)),
                ('voucher_disc_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('referral_disc_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('quantity', models.IntegerField(null=True)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('order_discount_amt', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('order_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('print_status', models.CharField(blank=True, choices=[('N', 'Not printed'), ('P', 'Printed')], default='PP', max_length=1)),
                ('cust_email_sent', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Order')),
                ('referral', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Referral')),
                ('shipper', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Shipper')),
                ('shipping_method', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Shipping_method')),
                ('shipping_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Shipping_status')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Ecom_site')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('voucher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Voucher')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice_user_image',
            fields=[
                ('invoice_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('item_unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_sub_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_disc_amt', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('moulding_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('print_medium_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('mount_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('board_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('acrylic_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('stretch_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('image_width', models.DecimalField(decimal_places=0, max_digits=3)),
                ('image_height', models.DecimalField(decimal_places=0, max_digits=3)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('acrylic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Acrylic')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Board')),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Cart_item')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Invoice')),
                ('moulding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Moulding')),
                ('mount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Mount')),
                ('print_medium', models.ForeignKey(default='PAPER', on_delete=django.db.models.deletion.PROTECT, to='artevenue.Print_medium')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Promotion')),
                ('stretch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Stretch')),
                ('user_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.User_image')),
            ],
            options={
                'abstract': False,
                'unique_together': {('invoice_item_id', 'invoice')},
            },
        ),
        migrations.CreateModel(
            name='Invoice_stock_image',
            fields=[
                ('invoice_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('item_unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_sub_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_disc_amt', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('moulding_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('print_medium_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('mount_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('board_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('acrylic_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('stretch_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('image_width', models.DecimalField(decimal_places=0, max_digits=3)),
                ('image_height', models.DecimalField(decimal_places=0, max_digits=3)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('acrylic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Acrylic')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Board')),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Cart_item')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Invoice')),
                ('moulding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Moulding')),
                ('mount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Mount')),
                ('print_medium', models.ForeignKey(default='PAPER', on_delete=django.db.models.deletion.PROTECT, to='artevenue.Print_medium')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Promotion')),
                ('stock_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.Stock_image')),
                ('stretch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Stretch')),
            ],
            options={
                'abstract': False,
                'unique_together': {('invoice_item_id', 'invoice')},
            },
        ),
        migrations.CreateModel(
            name='Invoice_stock_collage',
            fields=[
                ('invoice_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('item_unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_sub_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_disc_amt', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('moulding_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('print_medium_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('mount_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('board_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('acrylic_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('stretch_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('image_width', models.DecimalField(decimal_places=0, max_digits=3)),
                ('image_height', models.DecimalField(decimal_places=0, max_digits=3)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('acrylic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Acrylic')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Board')),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Cart_item')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Invoice')),
                ('moulding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Moulding')),
                ('mount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Mount')),
                ('print_medium', models.ForeignKey(default='PAPER', on_delete=django.db.models.deletion.PROTECT, to='artevenue.Print_medium')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Promotion')),
                ('stock_collage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.Stock_collage')),
                ('stretch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Stretch')),
            ],
            options={
                'abstract': False,
                'unique_together': {('invoice_item_id', 'invoice')},
            },
        ),
        migrations.CreateModel(
            name='Invoice_original_art',
            fields=[
                ('invoice_item_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('item_unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_sub_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_disc_amt', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('item_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('moulding_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('print_medium_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('mount_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('board_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('acrylic_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('stretch_size', models.DecimalField(decimal_places=2, max_digits=12, null=True)),
                ('image_width', models.DecimalField(decimal_places=0, max_digits=3)),
                ('image_height', models.DecimalField(decimal_places=0, max_digits=3)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('acrylic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Acrylic')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Board')),
                ('cart_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Cart_item')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Invoice')),
                ('moulding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Moulding')),
                ('mount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Mount')),
                ('original_art', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.Original_art')),
                ('print_medium', models.ForeignKey(default='PAPER', on_delete=django.db.models.deletion.PROTECT, to='artevenue.Print_medium')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Promotion')),
                ('stretch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Stretch')),
            ],
            options={
                'abstract': False,
                'unique_together': {('invoice_item_id', 'invoice')},
            },
        ),
    ]
