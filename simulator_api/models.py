from django.db import models


# Create your models here.

class Simulator(models.Model):
    ADDITIVE = "ADDITIVE"
    MULTIPLICATIVE = "MULTIPLICATIVE"
    time_series_choices = ((ADDITIVE, "Additive"), (MULTIPLICATIVE, "Multiplicative"))

    KAFKA = "KAFKA"
    CSV = "CSV"
    producer_type_choices = ((KAFKA, "Kafka"), (CSV, "CSV"))

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    use_case_name = models.CharField(max_length=200)
    time_series_type = models.CharField(choices=time_series_choices)
    meta_data = models.JSONField()
    producer_type = models.CharField(choices=producer_type_choices)
    process_id = models.IntegerField()


class Dataset(models.Model):
    SUBMITTED = "SUBMITTED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    status_choices = ((SUBMITTED, "Submitted"),
                      (RUNNING, "Running"),
                      (SUCCEEDED, "Succeeded"),
                      (FAILED, "Failed"))

    simulator = models.ForeignKey(Simulator, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=100)
    noise_level = models.CharField(max_length=100)
    trend_coefficients = models.JSONField()
    missing_percentage = models.FloatField()
    outlier_percentage = models.FloatField()
    cyclic_amplitude = models.FloatField()
    cyclic_frequency = models.FloatField()
    status = models.CharField(choices=status_choices)


class Seasonality(models.Model):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    frequency_choices = ((DAILY, "Daily"),
                         (WEEKLY, "Weekly"),
                         (MONTHLY, "Monthly"))

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    amplitude = models.FloatField()
    phase_shift = models.FloatField()
    frequency = models.CharField(choices=frequency_choices)
    frequency_multiplier = models.FloatField()
