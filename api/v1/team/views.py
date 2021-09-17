from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.team.models import Team
from api.v1.team.serializers import TeamSerializer, TeamStatSerializer


class TeamView(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamStatView(ListAPIView):
    serializer_class = TeamStatSerializer

    def get(self, request, *args, **kwargs):
        queryset = Team.objects.all()
        team_id = request.query_params.get('tid', None)
        if team_id:
            queryset = Team.objects.filter(id=team_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
