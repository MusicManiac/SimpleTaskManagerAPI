import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    # filters for the 'name' and 'description' fields to match partial strings (case-insensitive).
    name = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assigned_user']