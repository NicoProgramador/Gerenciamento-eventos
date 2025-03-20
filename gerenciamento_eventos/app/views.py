from django.shortcuts import render
from .models import Evento
from rest_framework.response import Response
from .serializers import EventoSerializer
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import EventoFilter
from rest_framework.generics import ListAPIView

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

class EventoListView(ListAPIView):
    serializer_class = EventoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventoFilter

    def get_queryset(self):
        evento = self.request.GET.get('evento', None)  # Pegando o filtro da URL
        queryset = Evento.objects.all()

        if evento:
            queryset = queryset.filter(categoriaEvento=evento)  # Filtrando dinamicamente
        
        return queryset
    
    def get_queryset2(self):
        evento = self.request.GET.get('evento', None)  # Pegando o filtro da URL
        queryset = Evento.objects.all()

        if evento:
            queryset = queryset.filter(dataHora=evento)  # Filtrando dinamicamente
        
        return queryset