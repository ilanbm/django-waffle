from django.db import connection
from django.contrib.sites.models import Site
from django.contrib.auth.models import AnonymousUser, Group, User

import waffle
from waffle.models import Flag, Sample, Switch
from waffle.tests.base import TestCase

from test_app import views

from waffle.tests.test_waffle import get, process_request


class SiteTests(TestCase):
    def setUp(self):
        super(SiteTests, self).setUp()
        Site.objects.create(id=2, domain='example2.com', name='example2.com')
        Site.objects.create(id=3, domain='example3.com', name='example3.com')
        Site.objects.create(id=4, domain='example4.com', name='example4.com')

        self.site1 = Site.objects.get(name='example.com')
        self.site2 = Site.objects.get(name='example2.com')
        self.site3 = Site.objects.get(name='example3.com')
        self.site4 = Site.objects.get(name='example4.com')

    def test_switch_by_site(self):
        """ test that we can get different switch values by site """
        name = 'myswitch'
        Switch.objects.create(name=name, active=True, site=self.site1,
                              all_sites_override=False)
        self.assertTrue(waffle.switch_is_active(get(), name))

        with self.settings(SITE_ID=2):
            self.assertFalse(waffle.switch_is_active(get(), name))

    def test_switch_all_sites_override(self):
        name = 'myswitch'
        Switch.objects.create(name=name, active=True, site=self.site1)
        self.assertTrue(waffle.switch_is_active(get(), name))

        with self.settings(SITE_ID=2):
            self.assertTrue(waffle.switch_is_active(get(), name))

    def test_switch_inactive_all_sites_override(self):
        name = 'myswitch'
        Switch.objects.create(name=name, active=False, site=self.site1)
        self.assertFalse(waffle.switch_is_active(get(), name))

        with self.settings(SITE_ID=2):
            self.assertFalse(waffle.switch_is_active(get(), name))

    def test_switch_by_multisite(self):
        name = "myswitch"
        switch1 = Switch.objects.create(name=name, active=True, site=self.site1,
                                        all_sites_override=False)
        switch1.site.add(self.site2)
        switch1.site.add(self.site3)

        self.assertTrue(waffle.switch_is_active(get(), name))
        with self.settings(SITE_ID=2):
            self.assertTrue(waffle.switch_is_active(get(), name))
        with self.settings(SITE_ID=3):
            self.assertTrue(waffle.switch_is_active(get(), name))
        with self.settings(SITE_ID=4):
            self.assertFalse(waffle.switch_is_active(get(), name))

    def test_switch_inactive_no_bound_sites(self):
        switch = Switch.objects.create(name='myswitch', active=True,
                                       all_sites_override=False)
        self.assertFalse(waffle.switch_is_active(get(), switch.name))

    def test_switch_site_default(self):
        name = 'myswitch'
        switch = Switch.objects.create(name=name, active=True)  # no site given

        self.assertTrue(waffle.switch_is_active(get(), name))

        with self.settings(SITE_ID=2):
            self.assertTrue(waffle.switch_is_active(get(), name))

    def test_get_switches_for_site(self):
        self.assertTrue(len(Switch.get_switches_for_site(self.site1)) == 0)
        name1 = "foo"
        Switch.objects.create(name=name1, active=True, site=self.site1)

        self.assertEqual([name1], [sw.name for sw in Switch.get_switches_for_site(self.site1)])
        # by default switch is sites-global
        self.assertEqual([name1], [sw.name for sw in Switch.get_switches_for_site(self.site2)])

        name2 = "bar"
        Switch.objects.create(name=name2, active=True, site=self.site2, all_sites_override=False)
        self.assertEqual({name1, name2}, set([sw.name for sw in Switch.get_switches_for_site(self.site2)]))
        self.assertEqual([name1], [sw.name for sw in Switch.get_switches_for_site(self.site1)])

    def test_sample_by_site(self):
        name = 'sample'
        Sample.objects.create(name=name, percent='100.0', site=self.site1,
                              all_sites_override=False)

        self.assertTrue(waffle.sample_is_active(get(), name))

        with self.settings(SITE_ID=2):
            self.assertFalse(waffle.sample_is_active(get(), name))

    def test_sample_all_sites_override(self):
        name = 'sample'
        Sample.objects.create(name=name, percent='100.0', site=self.site1)

        self.assertTrue(waffle.sample_is_active(get(), name))

        with self.settings(SITE_ID=2):
            self.assertTrue(waffle.sample_is_active(get(), name))

    def test_sample_inactive_all_sites_override(self):
        name = 'mysample'
        Sample.objects.create(name=name, percent='0.0', site=self.site1)
        self.assertFalse(waffle.sample_is_active(get(), name))

        with self.settings(SITE_ID=2):
            self.assertFalse(waffle.sample_is_active(get(), name))

    def test_sample_site_default(self):
        name = 'sample'
        sample = Sample.objects.create(name=name, percent='100.0') # no site given

        self.assertTrue(waffle.sample_is_active(get(), name))

        with self.settings(SITE_ID=2):
            self.assertTrue(waffle.sample_is_active(get(), name))
    
    def test_get_samples_for_site(self):
        self.assertTrue(len(Sample.get_samples_for_site(self.site1)) == 0)
        name1 = "foo"
        Sample.objects.create(name=name1, percent='100.0', site=self.site1)

        self.assertEqual([name1], [s.name for s in Sample.get_samples_for_site(self.site1)])
        # by default sample is sites-global
        self.assertEqual([name1], [s.name for s in Sample.get_samples_for_site(self.site2)])

        name2 = "bar"
        Sample.objects.create(name=name2, percent='0.0', site=self.site2, all_sites_override=False)
        self.assertEqual({name1, name2}, set([s.name for s in Sample.get_samples_for_site(self.site2)]))
        self.assertEqual([name1], [s.name for s in Sample.get_samples_for_site(self.site1)])

    def test_flag_by_site(self):
        name = 'myflag'
        flag1 = Flag.objects.create(name=name, everyone=True, site=self.site1,
                                    all_sites_override=False)
        request = get()

        response = process_request(request, views.flag_in_view)
        self.assertContains(response, b'on')

        with self.settings(SITE_ID=2):
            response = process_request(request, views.flag_in_view)
            self.assertContains(response, b'off')

    def test_flag_all_sites_override(self):
        name = 'sample'
        Flag.objects.create(name=name, everyone=True, site=self.site1)

        self.assertTrue(waffle.flag_is_active(get(), name))

        with self.settings(SITE_ID=2):
            self.assertTrue(waffle.flag_is_active(get(), name))

    def test_get_flags_for_site(self):
        self.assertTrue(len(Flag.get_flags_for_site(self.site1)) == 0)
        name1 = "foo"
        Flag.objects.create(name=name1, everyone=True, site=self.site1)

        self.assertEqual([name1], [f.name for f in Flag.get_flags_for_site(self.site1)])
        # by default sample is sites-global
        self.assertEqual([name1], [f.name for f in Flag.get_flags_for_site(self.site2)])

        name2 = "bar"
        Flag.objects.create(name=name2,  everyone=True, site=self.site2, all_sites_override=False)
        self.assertEqual({name1, name2}, set([f.name for f in Flag.get_flags_for_site(self.site2)]))
        self.assertEqual([name1], [f.name for f in Flag.get_flags_for_site(self.site1)])
