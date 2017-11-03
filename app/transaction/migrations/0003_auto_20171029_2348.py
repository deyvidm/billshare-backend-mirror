# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 23:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_auto_20171029_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionlineitem',
            name='creditor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creditors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transactionlineitem',
            name='debtor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debtors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transactionlineitem',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_line_items', to='transaction.Transaction'),
        ),
    ]
