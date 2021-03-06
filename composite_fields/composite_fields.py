from django.db import models


# TODO: Support for (recursive) composite fields having composite fields

class CompositeField:
    initialized = False
    fields = set()  # field names

    def __init__(self, name):
        self.name = name
        # self.fields = set()  # field names
        self.owner = None
        self.initialized = True

    def __str__(self):
        return self.name

    # Cannot use __getattr__ because it uses class attributes (fields) instead of this.
    def __getattribute__(self, item):
        if item in super().__getattribute__('fields'):
            return getattr(self.owner, self.name+'_'+item)
        if item == 'hash':
            return { f: getattr(self, f) for f in super().__getattribute__('fields') }
        if item == 'object':
            hash = self.hash
            return self.value_from_dict(hash)  # TODO: Shorten the code
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if self.initialized:  # not to be called in the constructor
            if key == 'hash':
                for key2, value2 in value.items():
                    setattr(self, key2, value2)
            if key == 'object':
                self.hash = self.value_to_dict(value)
            if key in self.fields:
                return setattr(self.owner, self.name + '_' + key, value)
        super().__setattr__(key, value)

    def value_from_dict(self, dict):
        return dict

    def value_to_dict(self, value):
        return value


# Internal
def my_filter(field_and_value):
    return isinstance(field_and_value[1], CompositeField)


# Internal
def my_filter2(field_and_value):
    return isinstance(field_and_value[1], models.fields.Field)


class ModelWithCompositeFields(models.Model):
    class Meta:
        abstract = True

    def __init__(self):
        # dir(type(self)) instead of type(self).__dict__  # also fields from base classes
        composite_fields = filter(my_filter, type(self).__dict__.items())
        values = []
        for field_name, composite_field in composite_fields:
            composite_field.owner = self
            for subfield_name, subfield in filter(my_filter2, type(composite_field).__dict__.items()):
                composite_field.fields.add(subfield_name)
                values.append((field_name+'_'+subfield_name, subfield))
                # setattr(self, field_name+'_'+subfield_name, subfield)  # FIXME: set on class, not instance
        for parent_fields in values:
            setattr(type(self), parent_fields[0], parent_fields[1])
        super().__init__()
