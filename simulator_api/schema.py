import graphene
from graphene_django import DjangoObjectType
from .models import Simulator, Dataset, Seasonality


class SimulatorType(DjangoObjectType):
    class Meta:
        model = Simulator
        fields = '__all__'


class DatasetType(DjangoObjectType):
    class Meta:
        model = Dataset
        fields = '__all__'


class SeasonalityType(DjangoObjectType):
    class Meta:
        model = Seasonality
        fields = '__all__'


class Query(graphene.ObjectType):
    all_simulators = graphene.List(SimulatorType)
    all_datasets = graphene.List(DatasetType)
    all_seasonalities = graphene.List(SeasonalityType)

    def resolve_all_simulators(root, info):
        return Simulator.objects.all()

    def resolve_all_datasets(root, info):
        return Dataset.objects.all()

    def resolve_all_seasonalities(root, info):
        return Seasonality.objects.all()


class CreateSeasonality(graphene.Mutation):
    class Arguments:
        frequency = graphene.String(required=True)
        multiplier = graphene.Int(required=True)
        phase_shift = graphene.Int(required=True)
        amplitude = graphene.Int(required=True)
        dataset_id = graphene.ID(required=True)
        pass

    seasonality = graphene.Field(SeasonalityType)

    def mutate(self, info, **kwargs):
        seasonality_obj = Seasonality.objects.create(frequency=kwargs['frequency'],
                                                     multiplier=kwargs['multiplier'],
                                                     phase_shift=kwargs['phase_shift'],
                                                     amplitude=kwargs['amplitude'],
                                                     dataset_id=kwargs['dataset_id'])

        # Return the created simulator object
        return CreateSeasonality(seasonality_obj)


class CreateSimulator(graphene.Mutation):
    class Arguments:
        # Simulator Arguments
        start_date = graphene.Date(required=True)
        end_date = graphene.Date(required=True)
        name = graphene.String(required=True)
        type = graphene.String(required=True)
        meta_data = graphene.JSONString(required=True)
        producer_type = graphene.String(required=True)
        sink_name = graphene.String(required=True)
        scheduled_interval_days = graphene.Int(required=True)

        pass

    simulator = graphene.Field(SimulatorType)

    def mutate(self, info, **kwargs):
        simulator_obj = Simulator.objects.create(start_date=kwargs['start_date'],
                                                 process_id=0,
                                                 end_date=kwargs['end_date'],
                                                 name=kwargs['name'],
                                                 type=kwargs['type'],
                                                 meta_data=kwargs['meta_data'],
                                                 producer_type=kwargs['producer_type'],
                                                 sink_name=kwargs['sink_name'],
                                                 scheduled_interval_days=kwargs['scheduled_interval_days'])

        # Return the created simulator object
        return CreateSimulator(simulator_obj)


class CreateDataset(graphene.Mutation):
    class Arguments:
        # Dataset Arguments
        frequency = graphene.String(required=True)
        noise_level = graphene.Float(required=True)
        trend_coefficients = graphene.JSONString(required=True)
        missing_percentage = graphene.Float(required=True)
        outlier_percentage = graphene.Float(required=True)
        cycle_amplitude = graphene.Float(required=True)
        cycle_frequency = graphene.Float(required=True)
        status = graphene.String(required=True)
        simulator_id = graphene.ID(required=True)
        pass

    dataset = graphene.Field(DatasetType)

    def mutate(self, info, **kwargs):
        dataset_obj = Dataset.objects.create(frequency=kwargs['frequency'],
                                             noise_level=kwargs['noise_level'],
                                             trend_coefficients=kwargs['trend_coefficients'],
                                             missing_percentage=kwargs['missing_percentage'],
                                             outlier_percentage=kwargs['outlier_percentage'],
                                             cycle_amplitude=kwargs['cycle_amplitude'],
                                             cycle_frequency=kwargs['cycle_frequency'],
                                             status=kwargs['status'],
                                             simulator_id=kwargs['simulator_id'])
        return CreateDataset(dataset_obj)


class Mutation(graphene.ObjectType):
    create_seasonality = CreateSeasonality.Field()
    create_dataset = CreateDataset.Field()
    create_simulator = CreateSimulator.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
