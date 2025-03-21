from django.shortcuts import render
from .models import Evento
from rest_framework.response import Response
from .serializers import EventoSerializer
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EventoFilter
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from datetime import datetime, timedelta
from django.http import JsonResponse

@api_view(['GET'])
def read_eventos(request):
    eventos = Evento.objects.all()
    serializer = EventoSerializer(eventos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def read_evento(request, pk):
    try:
        evento = Evento.objects.get(pk=pk)
    except Evento.DoesNotExist:
        return Response({'Erro: ': 'Esse evento não existe!'}, status=status.HTTP_404_NOT_FOUND)
    serializer = EventoSerializer(evento)
    return Response(serializer.data)

@api_view(['POST'])
def create_evento(request):
    if request.method == 'POST':
        serializer = EventoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'Erro: ': 'Esse evento não existe!'}, serializer.errors, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
def update_evento(request, pk):
    try:
        evento = Evento.objects.get(pk=pk)
    except Evento.DoesNotExist:
        return Response({'Erro: ': 'Esse evento não existe!'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EventoSerializer(evento, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_parcial_evento(request, pk):
    try:
        evento = Evento.objects.get(pk=pk)
    except Evento.DoesNotExist:
        return Response({'Erro: ': 'Esse evento não existe!'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = EventoSerializer(evento, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_evento(request, pk):
    try:
        evento = Evento.objects.get(pk=pk)
    except Evento.DoesNotExist:
        return Response({'Erro: ': 'Esse evento não existe!'}, status=status.HTTP_404_NOT_FOUND)
    
    evento.delete()
    return Response({"Mensagem: ": "Evento deletado com sucesso!"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_eventos_proximos(request):
    min_date_str = request.GET.get('min_date', None)
    max_date_str = request.GET.get('max_date', None)

    try:
        min_date = datetime.strptime(min_date_str, "%d/%m/%Y") if min_date_str else None
        max_date = datetime.strptime(max_date_str, "%d/%m/%Y") if max_date_str else None

        if max_date:
            max_date = max_date + timedelta(days=1) - timedelta(seconds=1)

        queryset = Evento.objects.all()

        if min_date and max_date:
            queryset = queryset.filter(dataHora__gte=min_date, dataHora__lte=max_date)
        elif min_date:
            queryset = queryset.filter(dataHora__gte=min_date)
        elif max_date:
            queryset = queryset.filter(dataHora__lte=max_date)

        serializer = EventoSerializer(queryset, many=True)
        return Response(serializer.data)

    except ValueError:
        return JsonResponse({'Erro': 'Formato de data inválido! Use DD/MM/YYYY'}, status=400)

class EventoListView(ListAPIView):
    serializer_class = EventoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = EventoFilter
    ordering_fields = ['dataHora']
    ordering = ['dataHora']

    def get_queryset(self):
        categoria = self.request.GET.get('evento', None)  # Pegando o filtro da URL
        quantidade = self.request.GET.get('quantidade', None)
        ordering = self.request.GET.get('ordering', None)
        
        queryset = Evento.objects.all()

        if categoria:
            queryset = queryset.filter(categoriaEvento=categoria)

        if ordering:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by('dataHora')

        if quantidade:
            try:
                quantidade = int(quantidade)
                queryset = queryset[:quantidade]
            except ValueError:
                pass

        return queryset