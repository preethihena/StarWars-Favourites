from rest_framework import serializers

from favourites.models import AbstractResourceModel


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractResourceModel
        fields = '__all__'
