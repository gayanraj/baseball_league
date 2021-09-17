from django.db.models import Sum
from rest_framework import serializers

from api.v1.match_player_stat.models import MatchPlayerStat
from api.v1.player.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class PlayerStatSerializer(serializers.ModelSerializer):
    stat = serializers.SerializerMethodField()

    class Meta:
        model = Player
        read_only_fields = ['stat']
        fields = ['id', 'name', 'nic', 'height', 'height_unit', 'team', 'stat']

    def get_stat(self, instance):
        player_stat_queryset = MatchPlayerStat.objects.filter(player=instance)
        total_matches = player_stat_queryset.count()
        score = 0
        if total_matches > 0:
            score = player_stat_queryset.aggregate(Sum('score')).get('score__sum')

        avg_score = None
        if total_matches > 0:
            avg_score = score / total_matches

        team = instance.team
        won_matches_queryset = player_stat_queryset.filter(match__winner_team=team)
        wins = won_matches_queryset.count()
        lost_matches_queryset = player_stat_queryset.filter(match__lost_team=team)
        loses = lost_matches_queryset.count()

        stat = {
            'total_matches': total_matches,
            'total_score': score,
            'average_score': avg_score,
            'wins': wins,
            'loses': loses
        }
        return stat
