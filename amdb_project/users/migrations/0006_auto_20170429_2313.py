# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 17:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20170429_1239'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Genres',
            new_name='Genre',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='user',
            new_name='user_id',
        ),
        migrations.AlterField(
            model_name='accesstoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users'),
        ),
    ]
