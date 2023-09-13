from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import SimulatorSerializer, DatasetSerializer, SeasonalitySerializer
from rest_framework.generics import ListAPIView
from rest_framework import viewsets, status
from .models import *
from configurers.django_configuration_manager import DjangoConfigurationManager


# Create your views here.


class SimulatorViewSet(viewsets.ModelViewSet):
    queryset = Simulator.objects.all()
    serializer_class = SimulatorSerializer

    def create(self, request, *args, **kwargs):
        simulator_data = request.data
        datasets_data = simulator_data.pop('datasets')
        seasonalities_data = datasets_data[0].pop('seasonality_components')

        simulator_serializer = SimulatorSerializer(data=simulator_data)
        simulator_data['meta_data'] = {}
        simulator_data['producer_type'] = 'csv'
        simulator_data['process_id'] = 0
        if simulator_serializer.is_valid():
            simulator_instance = simulator_serializer.save()
            for dataset_data in datasets_data:
                dataset_data['simulator'] = simulator_instance.id
                dataset_data['status'] = 'submitted'
                dataset_serializer = DatasetSerializer(data=dataset_data)
                if dataset_serializer.is_valid():
                    dataset_instance = dataset_serializer.save()
                    for seasonality_data in seasonalities_data:
                        seasonality_data['dataset'] = dataset_instance.id
                        seasonality_serializer = SeasonalitySerializer(data=seasonality_data)
                        if seasonality_serializer.is_valid():
                            seasonality_serializer.save()
                        else:
                            return Response(seasonality_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(dataset_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(simulator_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(simulator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        simulator_data = request.data

        # Serialize the author instance with the updated data
        simulator_serializer = SimulatorSerializer(instance, data=simulator_data, partial=True)

        if simulator_serializer.is_valid():
            simulator_serializer.save()

            return Response(simulator_serializer.data)
        else:
            return Response(simulator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def run_simulator(self, request, pk=None):
        instance = self.get_object()

        # TODO: add code to run the simulator here

        config_manager = DjangoConfigurationManager(simulator=instance)
        config_manager.load_config()
        config_manager.configure()
        # TODO: handle response from the simulator
        return Response({'message': "", 'result': ""}, status=status.HTTP_200_OK)