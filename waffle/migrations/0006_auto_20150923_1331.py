# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waffle', '0005_auto_20150923_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flag',
            name='site',
            field=models.ManyToManyField(related_name='waffle_flags_m2m', to='sites.Site', blank=True,
                                         help_text=b'utilized only if `all_sites_override` is set to False'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='site',
            field=models.ManyToManyField(related_name='waffle_samples_m2m', to='sites.Site', blank=True,
                                         help_text=b'utilized only if `all_sites_override` is set to False'),
        ),
        migrations.AlterField(
            model_name='switch',
            name='site',
            field=models.ManyToManyField(related_name='waffle_switches_m2m', to='sites.Site', blank=True,
                                         help_text=b'utilized only if `all_sites_override` is set to False'),
        ),
    ]
