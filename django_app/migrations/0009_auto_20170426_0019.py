# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 00:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0008_meetingnotthere'),
    ]

    operations = [
        migrations.AddField(
            model_name='meetingnotthere',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='meetingnotthere',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]