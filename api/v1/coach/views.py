from rest_framework import viewsets

from api.v1.coach.models import Coach
from api.v1.coach.serializers import CoachSerializer


class CoachView(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
