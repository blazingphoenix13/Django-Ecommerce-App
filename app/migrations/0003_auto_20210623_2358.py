# Generated by Django 3.0.7 on 2021-06-23 18:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20210623_2336'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderPlcaed',
            new_name='OrderPlaced',
        ),
        migrations.RenameField(
            model_name='orderplaced',
            old_name='order_date',
            new_name='ordered_date',
        ),
    ]
