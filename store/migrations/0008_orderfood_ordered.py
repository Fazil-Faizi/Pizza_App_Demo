# Generated by Django 3.2 on 2022-01-18 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_remove_orderfood_ordered'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderfood',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]