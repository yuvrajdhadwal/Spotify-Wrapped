from django.shortcuts import render
from rest_framework import viewsets
from .models import Song
from .serializers import SongSerializer

class SongViewSet(viewsets.ModelViewSet):
    """
    For testing, API endpoint that allows songs to be viewed or edited.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer