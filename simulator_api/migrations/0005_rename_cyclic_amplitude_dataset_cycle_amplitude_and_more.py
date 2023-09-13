# Generated by Django 4.2.5 on 2023-09-12 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0004_alter_seasonality_dataset'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='cyclic_amplitude',
            new_name='cycle_amplitude',
        ),
        migrations.RenameField(
            model_name='dataset',
            old_name='cyclic_frequency',
            new_name='cycle_frequency',
        ),
        migrations.RenameField(
            model_name='seasonality',
            old_name='frequency_multiplier',
            new_name='multiplier',
        ),
        migrations.RenameField(
            model_name='simulator',
            old_name='use_case_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='simulator',
            old_name='time_series_type',
            new_name='type',
        ),
    ]