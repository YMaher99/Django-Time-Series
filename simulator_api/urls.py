from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SimulatorViewSet
from graphene_django.views import GraphQLView
from simulator_api.schema import schema

router = DefaultRouter()
router.register(r'', SimulatorViewSet)

urlpatterns = [
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
    path('', include(router.urls), name="simulator")
]
