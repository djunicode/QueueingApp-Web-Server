from rest_framework import generics
from .serializers import LocationSerializer
from .models import Location


class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def platfrom_create(self, serializer):
        serializer.save()


class LocationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
