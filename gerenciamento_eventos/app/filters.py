import django_filters
from .models import Evento

class EventoFilter(django_filters.FilterSet):
    categoriaEvento = django_filters.CharFilter(field_name='categoriaEvento', lookup_expr='icontains', label='Categoria do Evento')
    dataHora = django_filters.DateTimeFilter(field_name='dataHora', lookup_expr='gte', label='Data e Hora (maior ou igual)')

    class Meta:
        model = Evento
        fields = ['categoriaEvento', 'dataHora']
