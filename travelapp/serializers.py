from rest_framework import serializers
from .models import *

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

    def create(self, validated_data):
        return Region.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.region_small = validated_data.get('region_small', instance.region_small)
        instance.region_large = validated_data.get('region_large', instance.region_large)
        instance.save()
        return instance


class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = '__all__'
