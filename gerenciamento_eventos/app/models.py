from django.db import models

class Evento(models.Model):
    nomeEvento = models.CharField(max_length=20)
    descricaoEvento = models.TextField(max_length=100, blank=False)
    dataHora = models.DateTimeField(blank=False)
    localEvento = models.CharField(max_length=20, blank=True)
    categoriaEvento = models.CharField(max_length=50, choices=(
        ("Musica", "Música"),
        ("Palestra", "Palestra"),
        ("Workshop", "Workshop")
    ))

    def __str__(self):
        return self.nomeEvento
