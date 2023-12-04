from ASSSs.models import House , Image
from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    house = HouseSerializer()

    class Meta:
        model = Image
        fields = '__all__'
