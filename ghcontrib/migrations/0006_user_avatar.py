# Generated by Django 2.0.2 on 2018-02-12 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghcontrib', '0005_auto_20180203_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.URLField(blank=True, null=True),
        ),
    ]
