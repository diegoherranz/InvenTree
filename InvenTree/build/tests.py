# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .models import Build
from part.models import Part

from InvenTree.status_codes import BuildStatus


class BuildTestSimple(TestCase):

    def setUp(self):
        part = Part.objects.create(name='Test part',
                                   description='Simple description')

        Build.objects.create(part=part,
                             batch='B1',
                             status=BuildStatus.PENDING,
                             title='Building 7 parts',
                             quantity=7,
                             notes='Some simple notes')

        Build.objects.create(part=part,
                             batch='B2',
                             status=BuildStatus.COMPLETE,
                             title='Building 21 parts',
                             quantity=21,
                             notes='Some simple notes')

    def test_build_objects(self):
        # Ensure the Build objects were correctly created
        self.assertEqual(Build.objects.count(), 2)
        b = Build.objects.get(pk=2)
        self.assertEqual(b.batch, 'B2')
        self.assertEqual(b.quantity, 21)

        self.assertEqual(str(b), 'Build 21 x Test part - Simple description')

    def test_url(self):
        b1 = Build.objects.get(pk=1)
        self.assertEqual(b1.get_absolute_url(), '/build/1/')

    def test_is_complete(self):
        b1 = Build.objects.get(pk=1)
        b2 = Build.objects.get(pk=2)

        self.assertEqual(b1.is_complete, False)
        self.assertEqual(b2.is_complete, True)

        self.assertEqual(b2.status, BuildStatus.COMPLETE)

    def test_is_active(self):
        b1 = Build.objects.get(pk=1)
        b2 = Build.objects.get(pk=2)

        self.assertEqual(b1.is_active, True)
        self.assertEqual(b2.is_active, False)

    def test_required_parts(self):
        # TODO - Generate BOM for test part
        pass

    def cancel_build(self):
        """ Test build cancellation function """

        build = Build.objects.get(id=1)

        self.assertEqual(build.status, BuildStatus.PENDING)

        build.cancelBuild()

        self.assertEqual(build.status, BuildStatus.CANCELLED)
