from rest_framework import serializers


class CountCityToQuerySerializer(serializers.Serializer):
    """Сериализатор для api"""
    name = serializers.CharField(max_length=250)
    count = serializers.IntegerField()
