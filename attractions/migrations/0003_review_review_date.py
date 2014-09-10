# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0002_auto_20140910_0528'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 10, 8, 52, 57, 623831), auto_now_add=True),
            preserve_default=False,
        ),
    ]
