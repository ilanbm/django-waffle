# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('waffle', '0003_auto_20150922_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='site',
            field=models.ManyToManyField(to='sites.Site', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='site',
            field=models.ManyToManyField(to='sites.Site', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='switch',
            name='site',
            field=models.ManyToManyField(to='sites.Site', null=True, blank=True),
        ),
    ]
