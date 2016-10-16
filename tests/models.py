from composite_fields.composite_fields import *


class MyCompositeField(CompositeField):
    field1 = models.fields.IntegerField()
    field2 = models.fields.IntegerField()


class MyModel(ModelWithCompositeFields):
    composite1 = MyCompositeField(name='composite1')
    composite2 = MyCompositeField(name='composite2')
