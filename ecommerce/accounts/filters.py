'''
from django.models import Orders
import .filters

class OrderFilter(filter_set.FilterSet):

    model = Orders
    fields = '__all__'
    '''

from .models import *
import django_filters
from django_filters import DateFilter, CharFilter
#from django_filters import DateFilter
#from django_filters import CharFilter


class OrderFilter(django_filters.FilterSet):
    #start_date = DateFilter(field_name = 'date_created', lookup_expr = 'gte')
    start_date = DateFilter(field_name = 'date_created', lookup_expr = 'gte')
    #end_date = DateFilter(field_name = 'date_created', lookup_expr = 'lte')
    end_date = DateFilter(field_name = 'date_created', lookup_expr = 'lte')
    note = CharFilter(field_name = 'note', lookup_expr = 'icontains')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']
