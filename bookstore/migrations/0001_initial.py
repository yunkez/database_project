# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ISBN', models.BigIntegerField()),
                ('title', models.CharField(max_length=100)),
                ('publisher', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('keywords', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('format', models.CharField(max_length=9, choices=[(b'hardcover', b'hardcover'), (b'softcover', b'softcover')])),
                ('year_of_publication', models.PositiveIntegerField()),
                ('price', models.PositiveIntegerField()),
                ('copies', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=100)),
                ('login_name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('card_number', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
                ('score', models.IntegerField(choices=[(1, b'1'), (2, b'2'), (3, b'3'), (4, b'4'), (5, b'5'), (6, b'6'), (7, b'7'), (8, b'8'), (9, b'9'), (10, b'10')])),
                ('book', models.ForeignKey(to='bookstore.Book')),
                ('customer', models.ForeignKey(to='bookstore.Customer')),
            ],
        ),
    ]
