from django_filters import fields, IsoDateTimeFilter
from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms import DateTimeField


class ListAsDictMixin(object):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        json_models = [model.as_dict() for model in page]
        return self.get_paginated_response(json_models)


# from https://stackoverflow.com/questions/14666199/how-do-i-create-multiple-model-instances-with-django-rest-framework
class CreateListModelMixin(object):
    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


# Use the CustomIsoDateTimeFilterMixin in a FilterSet. Makes all IsoDateTimeFilters within the FilterSet able to parse
# ISO 8601 datetimes, as well as all the other usual formats that the DateTimeFilter can do.
# https://django-filter.readthedocs.io/en/master/ref/fields.html#isodatetimefield
class CustomIsoDateTimeField(fields.IsoDateTimeField):
    input_formats = [fields.IsoDateTimeField.ISO_8601] + list(DateTimeField.input_formats)


class CustomIsoDateTimeFilterMixin(object):
    @classmethod
    def get_filters(cls):
        filters = super().get_filters()
        for f in filters.values():
            if isinstance(f, IsoDateTimeFilter):
                f.field_class = CustomIsoDateTimeField
        return filters


# This is useful to add to APIView to allow schema generation to infer its serializer output fields
# Along with setting this mixin, you should also set the `serializer_class` parameter like on the ViewSet class
class GetSerializerMixin(object):
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
        return self.serializer_class(*args, **kwargs)


# This is useful to add to APIView with `get` method to remove 'list' parameter and wrapping the return
# structure in an array which happens by default for get methods during schema generation
# It may need to go first in inheritance to make sure its init is called
class RetrieveMixin(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setattr(self, 'action', 'retrieve')
