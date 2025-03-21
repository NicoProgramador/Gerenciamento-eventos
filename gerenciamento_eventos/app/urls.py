from django.urls import path
from . import views
from .views import EventoListView

urlpatterns = [
    path('eventos/', views.read_eventos, name='read_eventos'),   
    path('eventos/<int:pk>', views.read_evento, name='read_evento'),
    path('eventos/criar', views.create_evento, name="create_evento"),
    path('eventos/atualizar/<int:pk>', views.update_evento, name='update_evento'),
    path('eventos/atualizarPartes/<int:pk>', views.update_parcial_evento, name='update_parcial_evento'),
    path('eventos/deletar/<int:pk>', views.delete_evento, name='delete_evento'),
    path('eventos/categorias/', EventoListView.as_view(), name="evento-list"),
    path('eventos/proximos/', views.get_eventos_proximos, name="get_eventos_proximos"),
]