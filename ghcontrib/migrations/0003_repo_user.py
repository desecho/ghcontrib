# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-14 20:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ghcontrib', '0002_repo'),
    ]

    operations = [
        migrations.AddField(
            model_name='repo',
            name='user',
            field=models.ForeignKey(
                default='',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='repos',
                to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
