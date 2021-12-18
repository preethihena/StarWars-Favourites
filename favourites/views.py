from django.http import JsonResponse
from rest_framework.views import APIView

from favourites.models import Planet
from favourites.serializers import ResourceSerializer
from favourites.swapiutils import SwapiService


def create_planet_response(serializer_data, swapi_data):
    response = {}
    response['custom_name'] = serializer_data['custom_name']
    response['is_favourite'] = serializer_data['is_favourite']
    response['updated'] = serializer_data['last_updated']
    response['name'] = swapi_data['name']
    response['url'] = swapi_data['url']
    response['created'] = swapi_data['created']
    return response


class SinglePlanetView(APIView):
    
    def post(self, request, **kwargs):
        swapi_service = SwapiService('planets')
        id = kwargs["id"]
        swapi_data = swapi_service.get_resource_by_id(id)
        if 'detail' in swapi_data.keys():
            return JsonResponse(status=201, data=swapi_data)
        planet_object, created = Planet.objects.get_or_create(id = id)
        serializer = ResourceSerializer(planet_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = create_planet_response(serializer.data, swapi_data)
            return JsonResponse(status=201, data=response)
        return JsonResponse(status=400, data="wrong parameters")
