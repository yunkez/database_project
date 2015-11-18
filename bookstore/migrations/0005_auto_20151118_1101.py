# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0004_auto_20151118_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
    ]
