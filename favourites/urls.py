from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from favourites import views

urlpatterns = [
    path('api/planets/<int:id>', views.SinglePlanetView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
