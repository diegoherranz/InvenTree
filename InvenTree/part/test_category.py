from django.test import TestCase

from .models import Part, PartCategory


class CategoryTest(TestCase):
    """
    Tests to ensure that the relational category tree functions correctly.

    Loads the following test fixtures:
    - category.yaml
    """
    fixtures = [
        'category',
        'part',
        'location',
    ]

    def setUp(self):
        # Extract some interesting categories for time-saving
        self.electronics = PartCategory.objects.get(name='Electronics')
        self.mechanical = PartCategory.objects.get(name='Mechanical')
        self.resistors = PartCategory.objects.get(name='Resistors')
        self.capacitors = PartCategory.objects.get(name='Capacitors')
        self.fasteners = PartCategory.objects.get(name='Fasteners')
        self.ic = PartCategory.objects.get(name='IC')
        self.transceivers = PartCategory.objects.get(name='Transceivers')

    def test_parents(self):
        """ Test that the parent fields are properly set,
        based on the test fixtures """

        self.assertEqual(self.resistors.parent, self.electronics)
        self.assertEqual(self.capacitors.parent, self.electronics)
        self.assertEqual(self.electronics.parent, None)

        self.assertEqual(self.fasteners.parent, self.mechanical)

    def test_children_count(self):
        """ Test that categories have the correct number of children """

        self.assertTrue(self.electronics.has_children)
        self.assertTrue(self.mechanical.has_children)

        self.assertEqual(len(self.electronics.children.all()), 3)
        self.assertEqual(len(self.mechanical.children.all()), 1)

    def test_unique_childs(self):
        """ Test the 'unique_children' functionality """

        childs = self.electronics.getUniqueChildren()

        self.assertIn(self.transceivers.id, childs)
        self.assertIn(self.ic.id, childs)

        self.assertNotIn(self.fasteners.id, childs)

    def test_unique_parents(self):
        """ Test the 'unique_parents' functionality """
        
        parents = self.transceivers.getUniqueParents()

        self.assertIn(self.electronics.id, parents)
        self.assertIn(self.ic.id, parents)
        self.assertNotIn(self.fasteners.id, parents)

    def test_path_string(self):
        """ Test that the category path string works correctly """

        self.assertEqual(str(self.resistors), 'Electronics/Resistors')
        self.assertEqual(str(self.transceivers), 'Electronics/IC/Transceivers')

    def test_url(self):
        """ Test that the PartCategory URL works """

        self.assertEqual(self.capacitors.get_absolute_url(), '/part/category/3/')

    def test_part_count(self):
        """ Test that the Category part count works """

        self.assertTrue(self.resistors.has_parts)
        self.assertTrue(self.fasteners.has_parts)
        self.assertFalse(self.transceivers.has_parts)

        self.assertEqual(self.fasteners.partcount(), 2)
        self.assertEqual(self.capacitors.partcount(), 1)

        self.assertEqual(self.electronics.partcount(), 3)

    def test_delete(self):
        """ Test that category deletion moves the children properly """

        # Delete the 'IC' category and 'Transceiver' should move to be under 'Electronics'
        self.assertEqual(self.transceivers.parent, self.ic)
        self.assertEqual(self.ic.parent, self.electronics)

        self.ic.delete()

        # Get the data again
        transceivers = PartCategory.objects.get(name='Transceivers')
        self.assertEqual(transceivers.parent, self.electronics)

        # Now delete the 'fasteners' category - the parts should move to 'mechanical'
        self.fasteners.delete()

        fasteners = Part.objects.filter(description__contains='screw')

        for f in fasteners:
            self.assertEqual(f.category, self.mechanical)

    def test_default_locations(self):
        """ Test traversal for default locations """

        self.assertEqual(str(self.fasteners.default_location), 'Office/Drawer_1')

        # Test that parts in this location return the same default location, too
        for p in self.fasteners.children.all():
            self.assert_equal(p.get_default_location(), 'Office/Drawer_1')

        # Any part under electronics should default to 'Home'
        R1 = Part.objects.get(name='R_2K2_0805')
        self.assertIsNone(R1.default_location)
        self.assertEqual(R1.get_default_location().name, 'Home')

        # But one part has a default_location set
        R2 = Part.objects.get(name='R_4K7_0603')
        self.assertEqual(R2.get_default_location().name, 'Bathroom')

        # And one part should have no default location at all
        W = Part.objects.get(name='Widget')
        self.assertIsNone(W.get_default_location())
