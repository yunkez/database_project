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
                ('login_name', models.CharField(unique=True, max_length=100)),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', models.BigIntegerField()),
                ('card_number', models.BigIntegerField()),
                ('address', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.PositiveIntegerField()),
                ('text', models.CharField(max_length=300)),
                ('book', models.ForeignKey(to='bookstore.Book')),
                ('customer', models.ForeignKey(to='bookstore.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('order_status', models.CharField(max_length=9, choices=[(b'submitted', b'submitted'), (b'executed', b'executed')])),
                ('book', models.ForeignKey(to='bookstore.Book')),
                ('customer', models.ForeignKey(to='bookstore.Customer')),
            ],
        ),
    ]
