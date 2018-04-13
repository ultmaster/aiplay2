# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-13 03:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0002_auto_20180410_0148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesolution',
            name='judge_report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='judge_report_set', to='program.RunningReport'),
        ),
        migrations.AlterField(
            model_name='gamesolution',
            name='user_report',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_report_set', to='program.RunningReport'),
        ),
    ]
