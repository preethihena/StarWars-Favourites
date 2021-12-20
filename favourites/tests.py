from rest_framework import status
from rest_framework.test import APITestCase

class SinglePlanetViewTests(APITestCase):
    def test_get_planet_for_correct_id(self):
        """
        Test if we are getting a planet for correct id.
        """
        url = '/api/planets/1/'
        planet_name = "Tatooine"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(planet_name, response.json().get("name"))
    
    def test_get_planet_for_wrong_id_returns_404(self):
        """
        Test if we are getting 404 for wrong planet id.
        """
        url = '/api/planets/70/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SinglePlanetFavouritesViewTests(APITestCase):
    def test_add_favourite_planet(self):
        """
        Adds a planet to favourites.
        """
        url_favourite = '/api/planets/1/favourite/'
        response = self.client.post(url_favourite)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_single_planet = '/api/planets/1/'
        response = self.client.get(url_single_planet)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json().get("is_favourite"))

    def test_remove_favourite_planet(self):
        """
        Removes a planet to favourites.
        """
        url_favourite = '/api/planets/1/favourite/'
        response = self.client.post(url_favourite) # Adding to Favourite
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url_favourite) # Removing from Favourite
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_single_planet = '/api/planets/1/'
        response = self.client.get(url_single_planet)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json().get("is_favourite"))

class PlanetCustomNameViewTests(APITestCase):
    def test_add_planet_custom_name_(self):
        """
        Adds Custom name to a planet
        """
        url_custom_name = '/api/planets/1/custom-name/'
        body = {'custom_name': 'test name'}
        response = self.client.post(url_custom_name, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_single_planet = '/api/planets/1/'
        response = self.client.get(url_single_planet)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('test name', response.json().get("custom_name"))

class FavouritePlanetViewTests(APITestCase):
    def test_get_all_favourite_planets_when_one_favourite(self):
        """
        Get all favourites return single object when only one favourite.
        """
        url_favourite = '/api/planets/1/favourite/'
        response = self.client.post(url_favourite) # Adding to Favourite
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_favourite_planets = '/api/planets/favourites/'
        response = self.client.get(url_favourite_planets)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 1)

    def test_get_all_favourite_planets_when_no_favourite(self):
        """
        Get all favourites returns empty when no favourites.
        """
        url_favourite_planets = '/api/planets/favourites/'
        response = self.client.get(url_favourite_planets)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 0)

    def test_get_all_favourite_planets_when_multiple_favourite(self):
        """
        Get all favourites test when multiple favourites.
        """
        url_favourite = '/api/planets/{0}/favourite/'
        response = self.client.post(url_favourite.format(1)) # Adding to Favourite
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url_favourite.format(2)) # Adding to Favourite
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_favourite_planets = '/api/planets/favourites/'
        response = self.client.get(url_favourite_planets)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 2)

class AllPlanetsViewTests(APITestCase):
    def test_get_all_planets(self):
        """
        Get all planet list without page number.
        Ensure we get page 1.
        """
        url = '/api/planets/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 10)
        self.assertIsNone(response.json().get("previous"))

    def test_get_all_planets_page_two(self):
        """
        Get Page 2 for all planet list. Ensure it is not empty.
        """
        url = '/api/planets/?page=2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 10)
        self.assertIsNotNone(response.json().get("previous"))

    def test_search_planet_based_on_name(self):
        """
        Ensure Search planet based on name working.
        """
        url = '/api/planets/?search=Tato'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("name"), "Tatooine")

class SingleMovieViewTests(APITestCase):
    def test_get_movie_for_correct_id(self):
        """
        Test if we are getting a movie for correct id.
        """
        url = '/api/movies/1/'
        planet_name = "A New Hope"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(planet_name, response.json().get("title"))
    
    def test_get_movie_for_wrong_id_returns_404(self):
        """
        Test if we are getting 404 for wrong movie id.
        """
        url = '/api/movies/70/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class SingleMovieFavouritesViewTests(APITestCase):
    def test_add_favourite_movie(self):
        """
        Adds a movie to favourites.
        """
        url_favourite = '/api/movies/1/favourite/'
        response = self.client.post(url_favourite)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_single_movie = '/api/movies/1/'
        response = self.client.get(url_single_movie)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json().get("is_favourite"))

    def test_remove_favourite_movie(self):
        """
        Removes a movie to favourites.
        """
        url_favourite = '/api/movies/1/favourite/'
        response = self.client.post(url_favourite) # Adding to Favourite
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url_favourite) # Removing from Favourite
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_single_movie = '/api/movies/1/'
        response = self.client.get(url_single_movie)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json().get("is_favourite"))

class MovieCustomNameViewTests(APITestCase):
    def test_add_movie_custom_name_(self):
        """
        Adds Custom name to a movie
        """
        url_custom_name = '/api/movies/1/custom-name/'
        body = {'custom_name': 'test name'}
        response = self.client.post(url_custom_name, body, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_single_movie = '/api/movies/1/'
        response = self.client.get(url_single_movie)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('test name', response.json().get("custom_name"))

class FavouriteMovieViewTests(APITestCase):
    def test_get_all_favourite_movies_when_one_favourite(self):
        """
        Get all favourites return single object when only one favourite.
        """
        url_favourite = '/api/movies/1/favourite/'
        response = self.client.post(url_favourite) # Adding to Favourite
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_favourite_movies = '/api/movies/favourites/'
        response = self.client.get(url_favourite_movies)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 1)

    def test_get_all_favourite_movies_when_no_favourite(self):
        """
        Get all favourites returns empty when no favourites.
        """
        url_favourite_movies = '/api/movies/favourites/'
        response = self.client.get(url_favourite_movies)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 0)

    def test_get_all_favourite_movies_when_multiple_favourite(self):
        """
        Get all favourites test when multiple favourites.
        """
        url_favourite = '/api/movies/{0}/favourite/'
        response = self.client.post(url_favourite.format(1)) # Adding to Favourite
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(url_favourite.format(2)) # Adding to Favourite
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url_favourite_movies = '/api/movies/favourites/'
        response = self.client.get(url_favourite_movies)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get("results")), 2)

class AllMoviesViewTests(APITestCase):
    def test_get_all_movies(self):
        """
        Get all movie list without page number.
        Ensure we get page 1.
        """
        url = '/api/movies/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.json().get("previous"))

    def test_get_all_movies_page_two(self):
        """
        Get page two of movies. Returns 404.
        """
        url = '/api/movies/?page=2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_search_movies_based_on_title(self):
        """
        Search movie test based on title of the movie.
        """
        url = '/api/movies/?search=hope'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json().get("results")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("title"), "A New Hope")
