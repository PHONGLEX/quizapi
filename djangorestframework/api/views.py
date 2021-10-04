from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Psi, AirTemperature
from .serializers import PsiSerializer, AirTemperatureSerializer, SearchDateSerializer
from .decorators import validate_datetime


class PsiPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = 'count'
    max_page_size = 1000
    page_query_param = 'p'


class PsiViewSet(ModelViewSet):
    serializer_class = PsiSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PsiPagination
    queryset = Psi.objects.all()

    @swagger_auto_schema(request_body=SearchDateSerializer)
    @action(detail=False, methods=['POST'])
    @validate_datetime
    def search(self, request, *args, **kwargs):
        try:
            param = kwargs.get('param')
            
            if param['type'] == 'date':
                
                data = Psi.objects.filter(Q(updated_timestamp__date=param['param']))
            elif param['type'] == 'datetime':
                data = Psi.objects.filter(Q(updated_timestamp=param['param']))

            if not data.exists():
                data = Psi.objects.filter(Q(updated_timestamp__date=Psi.objects.latest('updated_timestamp').updated_timestamp.date()))
            
            serializer = self.serializer_class(data, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Psi.DoesNotExist:
            return Response({"message": "the data matching query does not exist"}, status=status.HTTP_200_OK)


class AirTemperaturePagination(PageNumberPagination):
    page_size = 100
    max_page_size = 500
    page_size_query_param = "count"
    page_query_param ="p"


class AirTemperatureViewSet(ViewSet):
    serializer_class = AirTemperatureSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = AirTemperaturePagination

    def get_queryset(self):
        return AirTemperature.objects.all()

    def get_object(self):
        obj = AirTemperature.objects.get(pk=self.kwargs['pk'])
        return obj

    def list(self, request):
        queryset = AirTemperature.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AirTemperatureSerializer)
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = AirTemperature.objects.all()
        air_temperature = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(air_temperature)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AirTemperatureSerializer)
    def update(self, request, pk=None):
        airtemperature = self.get_object()
        data = request.data
        airtemperature.code = data.get('code')
        airtemperature.name = data.get('name')
        airtemperature.temperature = data.get('temperature')     
        airtemperature.save()

        serializer = self.serializer_class(airtemperature) 
        return Response(serializer.data)  

    @swagger_auto_schema(request_body=AirTemperatureSerializer)
    def partial_update(self, request, pk=None):
        airtemperature = self.get_object()
        data = request.data
        airtemperature.code = data.get('code', airtemperature.code)
        airtemperature.name = data.get('name', airtemperature.name)
        airtemperature.temperature = data.get('temperature', airtemperature.temperature)     
        airtemperature.save()

        serializer = self.serializer_class(airtemperature) 
        return Response(serializer.data)  

    def destroy(self, request, pk=None):
        airtemperature = self.get_object()
        airtemperature.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=SearchDateSerializer)
    @action(detail=False, methods=['POST'])
    @validate_datetime
    def search(self, request, *args, **kwargs):
        param = kwargs.get('param')
        
        if param.get('type') == 'date':
            data = AirTemperature.objects.filter(timestamp__date=param.get('param'))
        elif param.get('type') == 'datetime':
            data = AirTemperature.objects.filter(timestamp=param.get('param'))

        if not data.exists():
            data = AirTemperature.objects.filter(Q(timestamp__date=AirTemperature.objects.latest('timestamp').timestamp.date()))

        serializer = self.serializer_class(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)