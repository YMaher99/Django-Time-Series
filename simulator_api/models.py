from django.db import models
import warnings

warnings.simplefilter("ignore", category=Warning)


# Create your models here.

class Simulator(models.Model):
    """
        Model for storing data about simulators
    """

    ADDITIVE = "additive"
    MULTIPLICATIVE = "multiplicative"
    time_series_choices = ((ADDITIVE, "Additive"), (MULTIPLICATIVE, "Multiplicative"))

    KAFKA = "kafka"
    CSV = "csv"
    producer_type_choices = ((KAFKA, "Kafka"), (CSV, "CSV"))

    simulator_runner = None

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=200)
    type = models.CharField(choices=time_series_choices, max_length=200)
    meta_data = models.JSONField()
    producer_type = models.CharField(choices=producer_type_choices, max_length=200)
    process_id = models.IntegerField()
    sink_name = models.CharField(max_length=200, null=True)


class Dataset(models.Model):
    """
        Model for storing data about datasets
    """
    SUBMITTED = "submitted"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    status_choices = ((SUBMITTED, "Submitted"),
                      (RUNNING, "Running"),
                      (SUCCEEDED, "Succeeded"),
                      (FAILED, "Failed"))

    simulator = models.ForeignKey(Simulator, on_delete=models.CASCADE, related_name='datasets')
    frequency = models.CharField(max_length=100)
    noise_level = models.FloatField()
    trend_coefficients = models.JSONField()
    missing_percentage = models.FloatField()
    outlier_percentage = models.FloatField()
    cycle_amplitude = models.FloatField()
    cycle_frequency = models.FloatField()
    status = models.CharField(choices=status_choices, max_length=200)
    generator_id = models.CharField(max_length=200, null=True)
    attribute_id = models.CharField(max_length=200, null=True)


class Seasonality(models.Model):
    """
        Model for storing data about datasets
    """
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    frequency_choices = ((DAILY, "Daily"),
                         (WEEKLY, "Weekly"),
                         (MONTHLY, "Monthly"))

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="seasonality_components")
    amplitude = models.FloatField()
    phase_shift = models.FloatField()
    frequency = models.CharField(choices=frequency_choices, max_length=200)
    multiplier = models.FloatField()
