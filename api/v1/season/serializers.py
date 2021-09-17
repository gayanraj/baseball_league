from rest_framework import serializers

from api.v1.season.models import Season


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'
