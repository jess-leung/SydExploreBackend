# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('opening_hours', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField()),
                ('url', models.URLField(blank=True)),
                ('location', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to=b'')),
                ('category', models.CharField(max_length=3, choices=[(b'ADV', b'Adventurous'), (b'CUL', b'Cultural'), (b'EDU', b'Education'), (b'FUN', b'Fun'), (b'HIS', b'Historical'), (b'HUN', b'Hungry'), (b'LAZ', b'Lazy'), (b'LUX', b'Luxurious'), (b'NAT', b'Natural'), (b'SOC', b'Social')])),
                ('vote_adventurous', models.PositiveIntegerField(default=0)),
                ('vote_cultural', models.PositiveIntegerField(default=0)),
                ('vote_education', models.PositiveIntegerField(default=0)),
                ('vote_fun', models.PositiveIntegerField(default=0)),
                ('vote_historical', models.PositiveIntegerField(default=0)),
                ('vote_hungry', models.PositiveIntegerField(default=0)),
                ('vote_lazy', models.PositiveIntegerField(default=0)),
                ('vote_luxurious', models.PositiveIntegerField(default=0)),
                ('vote_natural', models.PositiveIntegerField(default=0)),
                ('vote_social', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review_text', models.TextField()),
                ('reviewer_name', models.CharField(max_length=200, blank=True)),
                ('review_title', models.CharField(max_length=200)),
                ('review_rating', models.PositiveIntegerField(default=0)),
                ('attraction', models.ForeignKey(to='attractions.Attraction')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
