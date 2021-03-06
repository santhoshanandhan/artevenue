# Generated by Django 2.1.4 on 2019-03-22 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artevenue', '0008_auto_20190322_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('wishlist_id', models.AutoField(primary_key=True, serialize=False)),
                ('session_id', models.CharField(blank=True, default='', max_length=40)),
                ('voucher_disc_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('quantity', models.IntegerField(null=True)),
                ('wishlist_sub_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('wishlist_disc_amt', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('wishlist_tax', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('wishlist_total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('updated_date', models.DateField(blank=True, null=True)),
                ('wishlist_status', models.CharField(blank=True, default='AC', max_length=2)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Ecom_site')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('voucher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Voucher')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist_original_art',
            fields=[
                ('wishlist_item_id', models.AutoField(primary_key=True, serialize=False)),
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
                ('updated_date', models.DateField(blank=True, null=True)),
                ('acrylic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Acrylic')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Board')),
                ('moulding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Moulding')),
                ('mount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Mount')),
                ('original_art', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.Original_art')),
                ('print_medium', models.ForeignKey(default='PAPER', on_delete=django.db.models.deletion.PROTECT, to='artevenue.Print_medium')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Promotion')),
                ('stretch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Stretch')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Wishlist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wishlist_stock_collage',
            fields=[
                ('wishlist_item_id', models.AutoField(primary_key=True, serialize=False)),
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
                ('updated_date', models.DateField(blank=True, null=True)),
                ('acrylic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Acrylic')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Board')),
                ('moulding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Moulding')),
                ('mount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Mount')),
                ('print_medium', models.ForeignKey(default='PAPER', on_delete=django.db.models.deletion.PROTECT, to='artevenue.Print_medium')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Promotion')),
                ('stock_collage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.Stock_collage')),
                ('stretch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Stretch')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Wishlist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wishlist_stock_image',
            fields=[
                ('wishlist_item_id', models.AutoField(primary_key=True, serialize=False)),
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
                ('updated_date', models.DateField(blank=True, null=True)),
                ('acrylic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Acrylic')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Board')),
                ('moulding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Moulding')),
                ('mount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Mount')),
                ('print_medium', models.ForeignKey(default='PAPER', on_delete=django.db.models.deletion.PROTECT, to='artevenue.Print_medium')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Promotion')),
                ('stock_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.Stock_image')),
                ('stretch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Stretch')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Wishlist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wishlist_user_image',
            fields=[
                ('wishlist_item_id', models.AutoField(primary_key=True, serialize=False)),
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
                ('updated_date', models.DateField(blank=True, null=True)),
                ('acrylic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Acrylic')),
                ('board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Board')),
                ('moulding', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Moulding')),
                ('mount', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Mount')),
                ('print_medium', models.ForeignKey(default='PAPER', on_delete=django.db.models.deletion.PROTECT, to='artevenue.Print_medium')),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Promotion')),
                ('stretch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='artevenue.Stretch')),
                ('user_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.User_image')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='artevenue.Wishlist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='wishlist_user_image',
            unique_together={('wishlist_item_id', 'wishlist')},
        ),
        migrations.AlterUniqueTogether(
            name='wishlist_stock_image',
            unique_together={('wishlist_item_id', 'wishlist')},
        ),
        migrations.AlterUniqueTogether(
            name='wishlist_stock_collage',
            unique_together={('wishlist_item_id', 'wishlist')},
        ),
        migrations.AlterUniqueTogether(
            name='wishlist_original_art',
            unique_together={('wishlist_item_id', 'wishlist')},
        ),
    ]
