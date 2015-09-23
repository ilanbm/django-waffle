# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waffle', '0003_auto_20150923_1102'),
    ]

    operations = [
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
