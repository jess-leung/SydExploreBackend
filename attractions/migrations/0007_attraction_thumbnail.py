# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attractions', '0006_auto_20140920_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='attraction',
            name='thumbnail',
            field=models.ImageField(default=0, upload_to=b'/attraction_images/thumbnails/', blank=True),
            preserve_default=False,
        ),
    ]
