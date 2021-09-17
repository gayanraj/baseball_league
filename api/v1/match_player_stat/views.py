from rest_framework import viewsets

from api.v1.match_player_stat.models import MatchPlayerStat
from api.v1.match_player_stat.serializers import MatchPlayerStatSerializer


class MatchPlayerStatView(viewsets.ModelViewSet):
    queryset = MatchPlayerStat.objects.all()
    serializer_class = MatchPlayerStatSerializer
