from rest_framework import serializers

from api.v1.coach.models import Coach


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'
