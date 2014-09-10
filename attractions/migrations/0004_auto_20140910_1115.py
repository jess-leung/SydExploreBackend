# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0003_review_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
