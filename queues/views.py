from rest_framework import generics
from .serializers import LocationSerializer
from .models import Location


class CreateView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def platfrom_create(self, serializer):
        serializer.save()


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
