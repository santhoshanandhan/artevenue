# Generated by Django 2.2.4 on 2020-01-14 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artevenue', '0081_auto_20191211_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='business_profile',
            name='business_code',
            field=models.CharField(blank=True, default='', max_length=8, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='business_profile',
            unique_together={('user', 'business_code')},
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone_number', models.CharField(blank=True, default='', max_length=30)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('', 'NA'), ('M', 'Male'), ('F', 'Female'), ('T', 'Not Specified')], default='', max_length=1)),
                ('business_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='artevenue.Business_profile')),
            ],
        ),
    ]
