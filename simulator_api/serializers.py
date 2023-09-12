from rest_framework import serializers
from .models import *


class SeasonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasonality
        fields = "__all__"


class DatasetSerializer(serializers.ModelSerializer):
    seasonality_components = SeasonalitySerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = '__all__'


class SimulatorSerializer(serializers.ModelSerializer):
    datasets = DatasetSerializer(many=True, read_only=True)

    class Meta:
        model = Simulator
        fields = "__all__"
