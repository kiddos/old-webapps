# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-03 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paperzapper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='document_content',
            field=models.BinaryField(null=True),
        ),
    ]
