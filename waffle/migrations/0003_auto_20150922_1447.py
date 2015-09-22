# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('waffle', '0002_auto_20150617_0749'),
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
        migrations.AlterUniqueTogether(
            name='flag',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='sample',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='switch',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='flag',
            name='site',
        ),
        migrations.RemoveField(
            model_name='sample',
            name='site',
        ),
        migrations.RemoveField(
            model_name='switch',
            name='site',
        ),
    ]
