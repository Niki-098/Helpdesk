from django_filters import rest_framework as filters
from .models import Ticket

class TicketFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    priority = filters.CharFilter(field_name='priority', lookup_expr='iexact')
    assigned_to = filters.NumberFilter(field_name='assigned_to__id')

    class Meta:
        model = Ticket
        fields = ['title', 'status', 'priority', 'assigned_to']
