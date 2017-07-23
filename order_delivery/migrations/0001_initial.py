# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-23 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_date', models.DateField(verbose_name='Delivery Date')),
                ('total_orders', models.IntegerField(default=0, verbose_name='Total Orders')),
                ('for_pesach', models.BooleanField(default=False, verbose_name='For Pesach')),
            ],
            options={
                'verbose_name_plural': 'deliveries',
            },
        ),
    ]