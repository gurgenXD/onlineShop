# Generated by Django 2.1.7 on 2019-03-12 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0046_auto_20190312_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='cars_list',
        ),
    ]
