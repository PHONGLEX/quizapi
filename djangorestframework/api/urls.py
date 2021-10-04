from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

router = DefaultRouter()
router.register('psi', views.PsiViewSet)
router.register('air-temperature', views.AirTemperatureViewSet, basename="air-temperature")


urlpatterns = [
    path('', include(router.urls))
]