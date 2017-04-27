# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 00:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_app', '0007_userconfirmation_conf_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeetingNotThere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(blank=True, max_length=200, null=True)),
                ('request_host', models.CharField(blank=True, max_length=200, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=400, null=True)),
                ('unique_phone_id', models.CharField(blank=True, max_length=400, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='not_theres', to='django_app.Meeting')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='not_theres', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]