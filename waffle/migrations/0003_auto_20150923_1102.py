# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def movie_data(apps, schema_editor):
    Flag = apps.get_model("waffle", "Flag")
    Switch = apps.get_model("waffle", "Switch")
    Sample = apps.get_model("waffle", "Sample")
    for flag in Flag.objects.all():
        flag.site_new.add(flag.site)
        flag.save()
    for switch in Switch.objects.all():
        switch.site_new.add(switch.site)
        switch.save()
    for sample in Sample.objects.all():
        sample.site_new.add(sample.site)
        sample.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('waffle', '0002_auto_20150617_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='flag',
            name='site_new',
            field=models.ManyToManyField(related_name='waffle_flags_m2m', null=True, to='sites.Site', blank=True),
        ),
        migrations.AddField(
            model_name='sample',
            name='site_new',
            field=models.ManyToManyField(related_name='waffle_samples_m2m', null=True, to='sites.Site', blank=True),
        ),
        migrations.AddField(
            model_name='switch',
            name='site_new',
            field=models.ManyToManyField(related_name='waffle_switches_m2m', null=True, to='sites.Site', blank=True),
        ),
        migrations.RunPython(movie_data),
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
    ]
