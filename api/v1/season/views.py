from rest_framework import viewsets

from api.v1.season.models import Season
from api.v1.season.serializers import SeasonSerializer


class SeasonView(viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
