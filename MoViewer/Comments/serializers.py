from rest_framework import serializers


class CommetsSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    user = serializers.CharField()
    movie = serializers.CharField()
    comment = serializers.CharField(max_length=250)
    created_at = serializers.DateTimeField()

