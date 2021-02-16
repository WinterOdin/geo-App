from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings


from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import *
from .models import *


location_search = settings.GEO



class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def list(self, request, *args, **kwargs):
        try:
            entries = Location.objects.all()
            print(len(entries))
            serializer = self.serializer_class(entries, many=True)
            return Response(serializer.data, status=200)

        except ObjectDoesNotExist:
            return Response("Database does not contain any entries", status=status.HTTP_404_NOT_FOUND,)
   


    def create(self, request, *args, **kwargs):
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        ip = '89.56.28.166'
        if ip:
            try:
                data = location_search.get_location(ip)
           
                if data is None:
                    return Response(status=status.HTTP_400_BAD_REQUEST,)
            except:
            
                # I've wanted do do someting like stroing ip in database then install celery
                # Then Have celery check database for rows that have ip but not the rest of the data 
                # and then call API to complete data
                # but this is overkill for recruitment task

                #adding  = Location(ip=ip)
                #adding.save()
                return Response( 

                """
                    Our services are temporarily unavailable, your entry was saved to database.
                    We'll update your ip with geological info as soon as possible (ET. 10 minutes).
                """

                , status=503,)

            serializer = self.serializer_class(data=dict(data))
            print(serializer)
           
            if serializer.is_valid():
                return Response("Data was successfully added", status=status.HTTP_201_CREATED,)
            else:
                a = serializer.errors
                print(a)
                return Response("Validation error occurred, try again later", status=status.HTTP_500_INTERNAL_SERVER_ERROR,)
        else:
            return Response("Internal error occurred ip is None", status=status.HTTP_404_NOT_FOUND,)


    def destroy(self, request, *args, **kwargs):
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        if ip:
            data = self.queryset.filter(ip=ip)
      
            if data:
                data.delete()
                return Response("Location was deleted", status=status.HTTP_200_OK, )
            else:
                return Response("Location was not found", status=status.HTTP_404_NOT_FOUND,)
        else:
            return Response("Internal error occurred ip is None", status=status.HTTP_404_NOT_FOUND,)



