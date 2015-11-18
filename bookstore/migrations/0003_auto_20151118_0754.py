# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0002_auto_20151117_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
