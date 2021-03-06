# Generated by Django 2.2.4 on 2020-09-10 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artist', '0015_generate_art_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist_original_art',
            name='unapproval_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='artist_original_art',
            name='unapproved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='artist_stock_image',
            name='unapproval_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='artist_stock_image',
            name='unapproved',
            field=models.BooleanField(default=False),
        ),
    ]
