from rest_framework import viewsets

from api.v1.match.models import Match
from api.v1.match.serializers import MatchSerializer


class MatchView(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
