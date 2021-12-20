from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from favourites import views

urlpatterns = [
    path('api/planets/<int:id>/', views.SinglePlanetView.as_view(), name='single-planet'),
    path('api/planets/<int:id>/favourite/', views.SinglePlanetFavouritesView.as_view(), name='single-planet-favourite'),
    path('api/planets/<int:id>/custom-name/', views.PlanetCustomNameView.as_view(), name='single-planet-custom-name'),
    path('api/planets/', views.AllPlanetView.as_view(), name='all-planets'),
    path('api/movies/<int:id>/', views.SingleMovieView.as_view(), name='single-movie'),
    path('api/movies/<int:id>/favourite/', views.SingleMovieFavouriteView.as_view(), name='single-movie-favourite'),
    path('api/movies/<int:id>/custom-name/', views.MoviesCustomNameView.as_view(), name='single-movie-custom-name'),
    path('api/movies/', views.AllMoviesView.as_view(), name='all-movies'),
    path('api/planets/<int:id>/movies/', views.MoviesByPlanetView.as_view(), name='single-planet-movies'),
    path('api/movies/favourites/', views.FavouriteMovieView.as_view(), name='favourite-movies'),
    path('api/planets/favourites/', views.FavouritePlanetView.as_view(), name='favourite-planets'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
