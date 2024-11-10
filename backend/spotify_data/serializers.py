'''docstring carl'''
from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    '''carl please put docstrings'''
    class Meta:
        '''carl please put docstrings youre crashing this for me too'''
        model = Song
        fields = '__all__'
