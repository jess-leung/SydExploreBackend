# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0007_attraction_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='attraction',
            name='latitude',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attraction',
            name='longitude',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=3),
            preserve_default=False,
        ),
    ]
