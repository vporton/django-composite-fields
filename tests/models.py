from composite_fields.composite_fields import *


class MyCompositeField(CompositeField):
    field1 = models.fields.IntegerField()
    field2 = models.fields.IntegerField()


class MyModel(ModelWithCompositeFields):
    composite1 = MyCompositeField('comp1')
    composite2 = MyCompositeField('comp2')
