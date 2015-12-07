# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waffle', '0006_auto_20150923_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='switch',
            name='all_sites_override',
            field=models.BooleanField(
                default=True,
                help_text=b"When True this switch is used for all sites"
                          b" IMPORTANT: don't allow to create two switches with the same name"),
        ),
        migrations.AddField(
            model_name='sample',
            name='all_sites_override',
            field=models.BooleanField(
                default=True,
                help_text=b"When True this sample is used for all sites"
                          b" IMPORTANT: don't allow to create two samples with the same name"),
        ),
        migrations.AddField(
            model_name='flag',
            name='all_sites_override',
            field=models.BooleanField(
                default=True,
                help_text=b"When True this flag is used for all sites"
                          b" IMPORTANT: don't allow to create two flags with the same name"),
        )
    ]
