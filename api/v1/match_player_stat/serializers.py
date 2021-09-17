from rest_framework import serializers

from api.v1.match_player_stat.models import MatchPlayerStat


class MatchPlayerStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchPlayerStat
        fields = '__all__'
