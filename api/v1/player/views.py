from rest_framework import viewsets, mixins, generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.v1.player.models import Player
from api.v1.player.serializers import PlayerSerializer, PlayerStatSerializer
from api.v1.player.util import PlayerUtil
from api.v1.team.models import Team


class PlayerView(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerStatSerializer


class PlayerStatView(ListAPIView):
    serializer_class = PlayerStatSerializer

    def get(self, request, *args, **kwargs):
        team_id = kwargs['team_id']
        team = Team.objects.get(id=team_id)
        queryset = Player.objects.filter(team=team)

        percentile = request.query_params.get('percentile', None)
        if percentile:
            try:
                percentile = float(percentile)
            except Exception:
                raise ValidationError('Invalid percentile value')
            queryset = PlayerUtil.filter_from_percentile(queryset, percentile)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
