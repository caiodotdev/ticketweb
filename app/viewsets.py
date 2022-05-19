from rest_framework import viewsets

from . import (
    serializers,
    models
)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TicketSerializer
    queryset = models.Ticket.objects.all()


class PackViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PackSerializer
    queryset = models.Pack.objects.all()


class ImagePackViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImagePackSerializer
    queryset = models.ImagePack.objects.all()
class ThreadViewSet(viewsets.ModelViewSet):
    
    serializer_class = serializers.ThreadSerializer
    queryset = models.Thread.objects.all()

