from django.db.models import Q, Sum
from rest_framework import serializers

from api.v1.match.models import Match
from api.v1.team.models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TeamStatSerializer(serializers.ModelSerializer):
    stat = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = '__all__'

    def get_stat(self, instance):
        win_queryset = Match.objects.filter(winner_team=instance)
        lose_queryset = Match.objects.filter(lost_team=instance)
        win_score = 0
        lose_score = 0
        if win_queryset.count() > 0:
            win_score = win_queryset.aggregate(Sum('winner_team_score')).get('winner_team_score__sum')
        if lose_queryset.count() > 0:
            lose_score = lose_queryset.aggregate(Sum('lost_team_score')).get('lost_team_score__sum')

        total_matches = win_queryset.count() + lose_queryset.count()
        total_score = win_score + lose_score
        average_score = None
        win_percentage = None
        if total_matches > 0:
            average_score = total_score / total_matches
            win_percentage = win_queryset.count() * 100 / total_matches

        stat = {
            'total_matches': total_matches,
            'wins': win_queryset.count(),
            'loses': lose_queryset.count(),
            'total_score': total_score,
            'average_score': average_score,
            'win_percentage': win_percentage
        }
        return stat
