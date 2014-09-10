# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attraction',
            name='image',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
    ]
