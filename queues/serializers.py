from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'room', 'department', 'floor', 'updated_at')
        read_only_fields = ('updated_at',)
