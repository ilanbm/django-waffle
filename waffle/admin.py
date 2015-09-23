from django.contrib import admin
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from waffle.models import Flag, Sample, Switch


def enable_for_all(ma, request, qs):
    # Iterate over all objects to cause cache invalidation.
    for f in qs.all():
        f.everyone = True
        f.save()
enable_for_all.short_description = 'Enable selected flags for everyone.'


def disable_for_all(ma, request, qs):
    # Iterate over all objects to cause cache invalidation.
    for f in qs.all():
        f.everyone = False
        f.save()
disable_for_all.short_description = 'Disable selected flags for everyone.'


class M2MSitesMixin(object):
    def get_sites(self, obj):
        return ",".join([x.domain for x in obj.site.all()])
    get_sites.short_description = _("Sites")


class M2MSitesListFilter(admin.SimpleListFilter):
    title = _("site")
    parameter_name = "site"

    def lookups(self, request, model_admin):
        return tuple(Site.objects.values_list('id', 'domain').
                     order_by('domain'))

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(site__in=[int(self.value())])


class FlagAdmin(M2MSitesMixin, admin.ModelAdmin):
    actions = [enable_for_all, disable_for_all]
    date_hierarchy = 'created'
    list_display = ('name', 'get_sites', 'note', 'everyone', 'percent', 'superusers',
                    'staff', 'authenticated', 'languages')
    list_filter = (M2MSitesListFilter, 'everyone', 'superusers', 'staff', 'authenticated')
    raw_id_fields = ('users', 'groups')
    ordering = ('-id',)


def enable_switches(ma, request, qs):
    for switch in qs:
        switch.active = True
        switch.save()
enable_switches.short_description = 'Enable the selected switches.'


def disable_switches(ma, request, qs):
    for switch in qs:
        switch.active = False
        switch.save()
disable_switches.short_description = 'Disable the selected switches.'


class SwitchAdmin(M2MSitesMixin, admin.ModelAdmin):
    actions = [enable_switches, disable_switches]
    date_hierarchy = 'created'
    list_display = ('name', 'get_sites', 'active', 'note', 'created', 'modified')
    list_filter = (M2MSitesListFilter, 'active',)
    ordering = ('-id',)


class SampleAdmin(M2MSitesMixin, admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('name', 'get_sites', 'percent', 'note', 'created', 'modified')
    list_filter = (M2MSitesListFilter, )
    ordering = ('-id',)


admin.site.register(Flag, FlagAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(Switch, SwitchAdmin)
