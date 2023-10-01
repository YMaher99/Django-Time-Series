import copy

from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import SimulatorSerializer, DatasetSerializer, SeasonalitySerializer
from rest_framework import viewsets, status
from .models import *
from configurers.django_configuration_manager import DjangoConfigurationManager
from generators.coefficients_generator import CoefficientsGenerator
from producers.csv_data_producer import CSVDataProducer
from producers.nifi_producer import NIFIProducer
from simulator_operations.parallel_run_simulator import ParallelRunSimulator


# Create your views here.


class SimulatorViewSet(viewsets.ModelViewSet):
    queryset = Simulator.objects.all()
    serializer_class = SimulatorSerializer

    simulator_runner = {}

    def create(self, request, *args, **kwargs) -> Response:
        """
            request: the request including the data of the simulator to be created
        Returns:
            Response: a response to the request
        """

        simulator_data = request.data
        simulator_serializer = SimulatorSerializer(data=simulator_data)
        simulator_data['meta_data'] = {}
        simulator_data['producer_type'] = 'csv'
        simulator_data['process_id'] = 0
        if simulator_serializer.is_valid():
            datasets_data = simulator_data.pop('datasets')
            simulator_instance = simulator_serializer.save()
            for dataset_data in datasets_data:
                dataset_data['simulator'] = simulator_instance.id
                dataset_data['status'] = 'submitted'
                dataset_serializer = DatasetSerializer(data=dataset_data)
                if dataset_serializer.is_valid():
                    seasonalities_data = dataset_data.pop('seasonality_components')
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

        """
            request: the request including the data of the simulator to be updated
        Returns:
            Response: a response to the request
        """
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
    def run_simulator(self, request, pk=None) -> Response:
        """
        Runs a simulator
        Args:
            request: ignored
            pk: primary key of the simulator to be run
        Returns:
            Response: a response to the request
        """
        instance = self.get_object()
        config_manager = DjangoConfigurationManager(instance)
        generator = CoefficientsGenerator(config_manager)
        if instance.producer_type == instance.CSV:
            producer = NIFIProducer()  # CSVDataProducer()
        else:
            producer = NIFIProducer()  # CSVDataProducer()

        if instance.simulator_runner is None:
            instance.simulator_runner = ParallelRunSimulator(config_manager, generator, producer)
        instance.simulator_runner.run_simulator()

        return Response({'message': "Simulator has started running"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def stop_simulator(self, request, pk=None):

        """
            stops a running simulator
        Args:
            request: ignored
            pk: primary key of the simulator to be run
        Returns:
            Response: a response to the request
        """
        instance = self.get_object()
        if instance.simulator_runner is not None:
            instance.simulator_runner.stop_simulator()
            instance.simulator_runner = None
        else:
            return Response({'message': "Simulator was not running"}, status=status.HTTP_200_OK)
        return Response({'message': "Simulator has stopped running"}, status=status.HTTP_200_OK)
