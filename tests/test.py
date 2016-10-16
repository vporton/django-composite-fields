from django.test import TestCase
from .models import *

class BaseUserGroupTestCase(TestCase):
    def setUp(self):
        self.model = MyModel()

    def test_fields(self):
        self.model.composite1.field1 = 1
        self.model.composite1.field2 = 2
        self.assertEqual(self.model.composite1.field1, 1)
        self.assertEqual(self.model.composite1.field2, 2)
        self.assertEqual(self.model.composite1_field1, 1)
        self.assertEqual(self.model.composite1_field2, 2)
        self.model.composite1_field1 = 3
        self.model.composite1_field2 = 4
        self.assertEqual(self.model.composite1.field1, 3)
        self.assertEqual(self.model.composite1.field2, 4)
        self.assertEqual(self.model.composite1_field1, 3)
        self.assertEqual(self.model.composite1_field2, 4)

        self.model.save()