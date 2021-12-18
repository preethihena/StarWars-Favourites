import requests
from django.http import JsonResponse
from rest_framework.views import APIView

from favourites.models import Movie, Planet
from favourites.serializers import MovieSerializer, PlanetSerializer
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
    def get(self, request, **kwargs):
        swapi_service = SwapiService('planets')
        id = kwargs["id"]
        swapi_data, status_code = swapi_service.get_resource_by_id(id)
        if status_code != requests.codes.ok:
            return JsonResponse(status=status_code, data=swapi_data)
        planet_object, created = Planet.objects.get_or_create(id = id)
        serializer = PlanetSerializer(planet_object)
        response = create_planet_response(serializer.data, swapi_data)
        return JsonResponse(data=response)

class SinglePlanetFavouritesView(APIView):
    def post(self, request, **kwargs):
        swapi_service = SwapiService('planets')
        id = kwargs["id"]
        swapi_data, status_code = swapi_service.get_resource_by_id(id)
        if status_code != requests.codes.ok:
            return JsonResponse(status=status_code, data=swapi_data)
        planet_object, created = Planet.objects.get_or_create(id = id)
        planet_object.is_favourite = not planet_object.is_favourite
        planet_object.save()
        return JsonResponse(status=201, data={"detail": "The item was updated successfully."})       

class PlanetCustomNameView(APIView):
    def post(self, request, **kwargs):
        swapi_service = SwapiService('planets')
        id = kwargs["id"]
        swapi_data, status_code = swapi_service.get_resource_by_id(id)
        if status_code != requests.codes.ok:
            return JsonResponse(status=status_code, data=swapi_data)
        planet_object, created = Planet.objects.get_or_create(id = id)
        custom_name = request.data.get("custom_name")
        serializer = PlanetSerializer(planet_object, data={"custom_name": custom_name}, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = create_planet_response(serializer.data, swapi_data)
            return JsonResponse(status=201, data=response)
        return JsonResponse(status=400, data={"details": "Wrong Parameters"})

class AllPlanetView(APIView):
    def get(self, request):
        swapi_service = SwapiService('planets')
        page = 1
        if "page" in request.GET.keys():
            page = request.GET.get("page")
        if "search" not in request.GET.keys():
            swapi_data, status_code = swapi_service.get_all_resources(page)
        else:
            search_value = request.GET.get("search")
            swapi_data, status_code = swapi_service.search(search_value, page)
        if status_code != requests.codes.ok:
            return JsonResponse(status=status_code, data=swapi_data)
        response = {}
        response["count"] = swapi_data["count"]
        response["next"] = swapi_data["next"]
        response["previous"] = swapi_data["previous"]
        response["results"] = []
        for planet in swapi_data['results']:
            id = int(planet['url'].split('/')[-2])
            planet_object, created = Planet.objects.get_or_create(id = id)
            serializer = PlanetSerializer(planet_object)
            response["results"].append(create_planet_response(serializer.data, planet))
        return JsonResponse(data=response)        

class SingleMovieView(APIView):
    def get(self, request, **kwargs):
        swapi_service = SwapiService('films')
        id = kwargs["id"]
        swapi_data, status_code = swapi_service.get_resource_by_id(id)
        if status_code != requests.codes.ok:
            return JsonResponse(status=status_code, data=swapi_data)
        movie_object, created = Movie.objects.get_or_create(id = id)
        serializer = MovieSerializer(movie_object)
        response = create_movie_response(serializer.data, swapi_data)
        return JsonResponse(data=response)

class SingleMovieFavouriteView(APIView):
     def post(self, request, **kwargs):
        swapi_service = SwapiService('films')
        id = kwargs["id"]
        swapi_data, status_code = swapi_service.get_resource_by_id(id)
        if status_code != requests.codes.ok:
            return JsonResponse(status=status_code, data=swapi_data)
        movie_object, created = Movie.objects.get_or_create(id = id)
        movie_object.is_favourite = not movie_object.is_favourite
        movie_object.save()
        return JsonResponse(status=201, data={"detail": "The item was updated successfully."})

class MoviesCustomNameView(APIView):
    def post(self, request, **kwargs):
        swapi_service = SwapiService('films')
        id = kwargs["id"]
        swapi_data, status_code = swapi_service.get_resource_by_id(id)
        if status_code != requests.codes.ok:
            return JsonResponse(status=status_code, data=swapi_data)
        movie_object, created = Movie.objects.get_or_create(id = id)
        custom_name = request.data.get("custom_name")
        serializer = MovieSerializer(movie_object, data={"custom_name": custom_name}, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = create_movie_response(serializer.data, swapi_data)
            return JsonResponse(status=201, data=response)
        return JsonResponse(status=400, data={"details": "Wrong Parameters"})

class AllMoviesView(APIView):
    def get(self, request):
        swapi_service = SwapiService('films')
        page = 1
        if "page" in request.GET.keys():
            page = request.GET.get("page")
        if "search" not in request.GET.keys():
            swapi_data, status_code = swapi_service.get_all_resources(page)
        else:
            search_value = request.GET.get("search")
            swapi_data, status_code = swapi_service.search(search_value, page)
        if status_code != requests.codes.ok:
            return JsonResponse(status=status_code, data=swapi_data)
        response = {}
        response["count"] = swapi_data["count"]
        response["next"] = swapi_data["next"]
        response["previous"] = swapi_data["previous"]
        response["results"] = []
        for movie in swapi_data['results']:
            id = int(movie['url'].split('/')[-2])
            movie_object, created = Movie.objects.get_or_create(id = id)
            serializer = MovieSerializer(movie_object)
            response["results"].append(create_movie_response(serializer.data, movie))
        return JsonResponse(data=response)

class MoviesByPlanetView(APIView):
    def get(self, request, **kwargs):
        swapi_service_planet = SwapiService("planets")
        id = kwargs["id"]
        swapi_data, status_code = swapi_service_planet.get_resource_by_id(id)
        if status_code != requests.codes.ok:
            return JsonResponse(status=status_code, data=swapi_data)
        response = {}
        response["results"] = []
        swapi_service_movie = SwapiService("films")
        for movie_url in swapi_data["films"]:
            id = int(movie_url.split('/')[-2])
            movie, status_code = swapi_service_movie.get_resource_by_id(id)
            movie_object, created = Movie.objects.get_or_create(id = id)
            serializer = MovieSerializer(movie_object)
            response["results"].append(create_movie_response(serializer.data, movie))
        return JsonResponse(data=response)

class FavouriteMovieView(APIView):
    def get(self, request, **kwargs):
        swapi_service = SwapiService("films")
        movie_list = Movie.objects.filter(is_favourite=True)
        response = {"results": []}
        for movie_object in movie_list:
            movie, status_code = swapi_service.get_resource_by_id(movie_object.id)
            serializer = MovieSerializer(movie_object)
            response["results"].append(create_movie_response(serializer.data, movie))
        return JsonResponse(data=response)

class FavouritePlanetView(APIView):
    def get(self, request, **kwargs):
        swapi_service = SwapiService("planets")
        planet_list = Planet.objects.filter(is_favourite=True)
        response = {"results": []}
        for planet_object in planet_list:
            planet, status_code = swapi_service.get_resource_by_id(planet_object.id)
            serializer = PlanetSerializer(planet_object)
            response["results"].append(create_planet_response(serializer.data, planet))
        return JsonResponse(data=response)
