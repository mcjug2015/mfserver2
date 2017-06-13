# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-12 23:55
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CigarShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cigar_shops', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.IntegerField(choices=[(1, 'Sunday'), (2, 'Monday'), (3, 'Tuesday'), (4, 'Wednesday'), (5, 'Thursday'), (6, 'Friday'), (7, 'Saturday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(max_length=300)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('geo_location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('is_active', models.BooleanField(default=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meetings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingNotThere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(blank=True, max_length=200, null=True)),
                ('request_host', models.CharField(blank=True, max_length=200, null=True)),
                ('user_agent', models.CharField(blank=True, max_length=400, null=True)),
                ('unique_phone_id', models.CharField(blank=True, max_length=400, null=True)),
                ('resolved', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='not_theres', to='django_app.Meeting')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='not_theres', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MeetingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='UserConfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expiration_date', models.DateTimeField()),
                ('confirmation_key', models.CharField(max_length=64)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('confirmation_date', models.DateTimeField(blank=True, null=True)),
                ('conf_type', models.CharField(default='registration', max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confirmations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='types',
            field=models.ManyToManyField(blank=True, related_name='meetings', to='django_app.MeetingType'),
        ),
        migrations.CreateModel(
            name='MapMeeting',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('django_app.meeting',),
        ),
    ]
