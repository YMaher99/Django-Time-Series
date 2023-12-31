# Generated by Django 4.2.5 on 2023-11-07 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0007_dataset_attribute_id_dataset_generator_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulator',
            name='producer_type',
            field=models.CharField(choices=[('kafka', 'Kafka'), ('csv', 'CSV'), ('nifi', 'NIFI')], max_length=200),
        ),
    ]
