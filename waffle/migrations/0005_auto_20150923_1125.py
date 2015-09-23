# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('waffle', '0004_auto_20150923_1120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flag',
            old_name='site_new',
            new_name='site',
        ),
        migrations.RenameField(
            model_name='sample',
            old_name='site_new',
            new_name='site',
        ),
        migrations.RenameField(
            model_name='switch',
            old_name='site_new',
            new_name='site',
        ),
    ]
