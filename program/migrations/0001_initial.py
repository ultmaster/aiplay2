# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-05 10:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('language', models.CharField(choices=[('cpp', 'C++'), ('java', 'Java'), ('py', 'Python'), ('js', 'Javascript')], max_length=12)),
                ('workspace', models.CharField(max_length=192)),
                ('is_compiled', models.IntegerField(choices=[(0, 'Unknown'), (1, 'Success'), (2, 'Failed')], default=0)),
                ('compiler_message', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RunningReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_output', models.TextField(blank=True)),
                ('time_consumption', models.FloatField(default=0)),
                ('return_code', models.IntegerField(default=0)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.Code')),
            ],
        ),
    ]
