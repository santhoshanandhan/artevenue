# Generated by Django 2.2.4 on 2020-01-24 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artevenue', '0088_delete_business_commission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business_referral_fee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month_year', models.CharField(help_text='Commission month (YYYY-MM)', max_length=7)),
                ('ord_value_ytd', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('fee_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('fee_paid_date', models.DateTimeField(null=True)),
                ('fee_paid_reference', models.CharField(blank=True, default='', max_length=600)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('business_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.Business_profile')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artevenue.Order')),
            ],
        ),
    ]
