from composite_fields.composite_fields import *


class MyCompositeField(CompositeField):
    field1 = models.fields.IntegerField()
    field2 = models.fields.IntegerField()

    def value_from_dict(self, dict):
        return str(dict['field1']) + '/' + str(dict['field2'])

    def value_to_dict(self, value):
        arr = value.split('/')
        return { 'field1': int(arr[0]), 'field2': int(arr[1]) }


class MyModel(ModelWithCompositeFields):
    composite1 = MyCompositeField(name='composite1')
    composite2 = MyCompositeField(name='composite2')
