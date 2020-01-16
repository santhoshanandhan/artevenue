# Generated by Django 2.2.4 on 2019-11-06 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artevenue', '0062_auto_20191105_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter_subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('subscription_active', models.BooleanField(default=False)),
                ('subscription_start_date', models.DateField(blank=True, null=True)),
                ('subscription_end_date', models.DateField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
