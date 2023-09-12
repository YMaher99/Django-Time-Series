from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SimulatorViewSet

router = DefaultRouter()
router.register(r'', SimulatorViewSet)

urlpatterns = [
    path('', include(router.urls), name="simulator")
]
