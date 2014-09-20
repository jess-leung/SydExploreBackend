# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0005_attraction_vote_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attraction',
            name='image',
            field=models.ImageField(upload_to=b'/attraction_images/', blank=True),
        ),
    ]
