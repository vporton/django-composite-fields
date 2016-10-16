from django.test import TestCase
from composite_fields.composite_fields import *


class MyCompositeField(CompositeField):
    field1 = models.fields.IntegerField()
    field2 = models.fields.IntegerField()


class MyModel(ModelWithCompositeFields):
    composite1 = MyCompositeField(name='composite1')
    composite2 = MyCompositeField(name='composite2')


class BaseUserGroupTestCase(TestCase):
    def setUp(self):
        self.model = MyModel()

    def test_fields(self):
        self.model.composite1.field1 = 1
        self.model.composite1.field2 = 2
        self.assertEqual(self.model.composite1.field1, 1)  # FIXME: It does not user __getattr__ but instead static attribute
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