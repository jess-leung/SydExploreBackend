# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0004_auto_20140910_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='attraction',
            name='vote_category',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
