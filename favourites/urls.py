from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from favourites import views

urlpatterns = [
    path('api/planets/<int:id>', views.SinglePlanetView.as_view()),
    path('api/planets/', views.AllPlanetView.as_view()),
    path('api/movies/<int:id>', views.SingleMovieView.as_view()),
    path('api/movies/', views.AllMoviesView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
