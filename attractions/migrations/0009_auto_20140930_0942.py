# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0008_auto_20140930_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attraction',
            name='latitude',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='attraction',
            name='longitude',
            field=models.CharField(max_length=10),
        ),
    ]
