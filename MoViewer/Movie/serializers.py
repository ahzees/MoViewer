from rest_framework.views import APIView
from rest_framework.response import Response

from Movie.models import *
from rest_framework import serializers

class MovieSerializer(serializers.Serializer):
    description = serializers.CharField()
    name = serializers.CharField(max_length=255)
    video = serializers.FileField()
    images = serializers.ImageField()
    year = serializers.DateField()

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.name = validated_data.get('name',instance.name)
        instance.video = validated_data.get('video',instance.video)
        instance.images = validated_data.get('images',instance.images)
        instance.year = validated_data.get('year',instance.year)
        instance.save()
        return instance