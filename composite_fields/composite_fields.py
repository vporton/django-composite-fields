from django.db import models


# TODO: Support for (recursive) composite fields having composite fields

class CompositeField:
    initialized = False

    def __init__(self, name):
        self.name = name
        self.fields = set()
        self.owner = None
        self.initialized = True

    def __str__(self):
        return self.name

    def __getattr__(self, item):
        if item in self.fields:
            return getattr(self.owner, self.name+'_'+item)
        raise AttributeError

    def __setattr__(self, key, value):
        if self.initialized:  # not to be called in the constructor
            if key in self.fields:
                return setattr(self.owner, self.name + '_' + key, value)
        super().__setattr__(key, value)


class ModelWithCompositeFields(models.Model):
    def __init__(self):
        # dir(type(self)) instead of self.__dict__  # also fields from base classes
        for field_name in filter(lambda field: isinstance(field, CompositeField), self.__dict__):
            composite_field = type(self).field_name
            for subfield in filter(lambda subfield: isinstance(subfield, models.fields.Field), composite_field.fields):
                composite_field.fields.add(subfield.name)
                setattr(self, field_name+'_'+subfield.name, subfield)
                composite_field.owner = self
        super().__init__()
