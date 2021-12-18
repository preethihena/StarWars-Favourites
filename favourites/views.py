from django.http import JsonResponse
from rest_framework.views import APIView

from favourites.models import Movie, Planet
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

def create_movie_response(serializer_data, swapi_data):
    response = {}
    response['custom_name'] = serializer_data['custom_name']
    response['is_favourite'] = serializer_data['is_favourite']
    response['updated'] = serializer_data['last_updated']
    response['title'] = swapi_data['title']
    response['url'] = swapi_data['url']
    response['created'] = swapi_data['created']
    response['release_date'] = swapi_data['release_date']
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
    
    def get(self, request, **kwargs):
        swapi_service = SwapiService('planets')
        id = kwargs["id"]
        swapi_data = swapi_service.get_resource_by_id(id)
        if 'detail' in swapi_data.keys():
            return JsonResponse(status=200, data=swapi_data)
        planet_object, created = Planet.objects.get_or_create(id = id)
        serializer = ResourceSerializer(planet_object)
        response = create_planet_response(serializer.data, swapi_data)
        return JsonResponse(data=response)


class AllPlanetView(APIView):
    def get(self, request):
        swapi_service = SwapiService('planets')
        page = 1
        if "page" in request.GET.keys():
            page = request.GET.get("page")
        if "search" not in request.GET.keys():
            swapi_data = swapi_service.get_all_resources(page)
        else:
            search_value = request.GET.get("search")
            swapi_data = swapi_service.search(search_value, page)
        if "detail" in swapi_data.keys():
            return JsonResponse(status=200, data=swapi_data)
        if len(swapi_data["results"]) == 0:
            return JsonResponse(status=200, data=swapi_data)
        response = {}
        response["count"] = swapi_data["count"]
        response["next"] = swapi_data["next"]
        response["previous"] = swapi_data["previous"]
        response["results"] = []
        for planet in swapi_data['results']:
            id = int(planet['url'].split('/')[-2])
            planet_object, created = Planet.objects.get_or_create(id = id)
            serializer = ResourceSerializer(planet_object)
            response["results"].append(create_planet_response(serializer.data, planet))
        return JsonResponse(data=response)
            

class SingleMovieView(APIView):
    def post(self, request, **kwargs):
        swapi_service = SwapiService('films')
        id = kwargs["id"]
        swapi_data = swapi_service.get_resource_by_id(id)
        if 'detail' in swapi_data.keys():
            return JsonResponse(status=201, data=swapi_data)
        movie_object, created = Movie.objects.get_or_create(id = id)
        serializer = ResourceSerializer(movie_object, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = create_movie_response(serializer.data, swapi_data)
            return JsonResponse(status=201, data=response)
        return JsonResponse(status=400, data="wrong parameters")
    
    def get(self, request, **kwargs):
        swapi_service = SwapiService('films')
        id = kwargs["id"]
        swapi_data = swapi_service.get_resource_by_id(id)
        if 'detail' in swapi_data.keys():
            return JsonResponse(status=200, data=swapi_data)
        movie_object, created = Movie.objects.get_or_create(id = id)
        serializer = ResourceSerializer(movie_object)
        response = create_movie_response(serializer.data, swapi_data)
        return JsonResponse(data=response)

class AllMoviesView(APIView):
    def get(self, request):
        swapi_service = SwapiService('films')
        page = 1
        if "page" in request.GET.keys():
            page = request.GET.get("page")
        if "search" not in request.GET.keys():
            swapi_data = swapi_service.get_all_resources(page)
        else:
            search_value = request.GET.get("search")
            swapi_data = swapi_service.search(search_value, page)
        if "detail" in swapi_data.keys():
            return JsonResponse(status=200, data=swapi_data)
        if len(swapi_data["results"]) == 0:
            return JsonResponse(status=200, data=swapi_data)
        response = {}
        response["count"] = swapi_data["count"]
        response["next"] = swapi_data["next"]
        response["previous"] = swapi_data["previous"]
        response["results"] = []
        for movie in swapi_data['results']:
            id = int(movie['url'].split('/')[-2])
            movie_object, created = Movie.objects.get_or_create(id = id)
            serializer = ResourceSerializer(movie_object)
            response["results"].append(create_movie_response(serializer.data, movie))
        return JsonResponse(data=response)

class MoviesByPlanetView(APIView):

    def get(self, request, **kwargs):
        swapi_service_planet = SwapiService("planets")
        id = kwargs["id"]
        swapi_data = swapi_service_planet.get_resource_by_id(id)
        if 'detail' in swapi_data.keys():
            return JsonResponse(status=200, data=swapi_data)
        response = {}
        response["results"] = []
        swapi_service_movie = SwapiService("films")
        for movie_url in swapi_data["films"]:
            id = int(movie_url.split('/')[-2])
            movie = swapi_service_movie.get_resource_by_id(id)
            movie_object, created = Movie.objects.get_or_create(id = id)
            serializer = ResourceSerializer(movie_object)
            response["results"].append(create_movie_response(serializer.data, movie))
        return JsonResponse(data=response)


class FavouriteMovieView(APIView):
    def get(self, request, **kwargs):
        swapi_service = SwapiService("films")
        movie_list = Movie.objects.filter(is_favourite=True)
        response = {"results": []}
        for movie_object in movie_list:
            movie = swapi_service.get_resource_by_id(movie_object.id)
            serializer = ResourceSerializer(movie_object)
            response["results"].append(create_movie_response(serializer.data, movie))
        return JsonResponse(data=response)

class FavouritePlanetView(APIView):
    def get(self, request, **kwargs):
        swapi_service = SwapiService("planets")
        planet_list = Planet.objects.filter(is_favourite=True)
        response = {"results": []}
        for planet_object in planet_list:
            planet = swapi_service.get_resource_by_id(planet_object.id)
            serializer = ResourceSerializer(planet_object)
            response["results"].append(create_planet_response(serializer.data, planet))
        return JsonResponse(data=response)
