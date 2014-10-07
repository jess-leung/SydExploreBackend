# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0009_auto_20140930_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_category',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]
