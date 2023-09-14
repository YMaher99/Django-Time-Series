from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import Client


# Create your tests here.

class APITestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_simulators_endpoint(self):
        response = self.client.get(path='/simulator/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_simulators_endpoint(self):
        data = {
            "name": "simulator1",
            "start_date": "2021-01-01",
            "end_date": "2022-01-01",
            "type": "additive",
            "datasets": [
                {

                    "frequency": "1H",

                    "trend_coefficients": [0, 2, 1, 3],

                    "missing_percentage": 0.06,

                    "outlier_percentage": 10,

                    "noise_level": 10,

                    "cycle_amplitude": 3,

                    "cycle_frequency": 1,

                    "seasonality_components": [

                        {

                            "frequency": "Weekly",

                            "multiplier": 1,

                            "phase_shift": 0,

                            "amplitude": 3

                        },

                        {

                            "frequency": "Daily",

                            "multiplier": 2,

                            "phase_shift": 90,

                            "amplitude": 5

                        }

                    ]

                }
            ]

        }
        response = self.client.post(path='/simulator/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_run_simulator(self):
        response = self.client.get(path='/simulator/8/run_simulator/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stop_simulator(self):
        response = self.client.get(path='/simulator/8/stop_simulator/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
