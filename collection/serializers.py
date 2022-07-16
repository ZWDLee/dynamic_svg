from rest_framework import serializers
from .models import Collection, CollectionSvgList

class CollectionSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Collection
        fields = ('id', 'coll_name', 'author', 'package', 'created_date')

class CollectionSvgListSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    coll_name = serializers.ReadOnlyField()
    svg_code = serializers.ReadOnlyField()
    svg_name = serializers.ReadOnlyField()
    class Meta:
        model = CollectionSvgList
        fields = ('id', 'svg', 'svg_code', 'svg_name', 'collection', 'coll_name', 'created_date')

# class CollectionCountSerializer(serializers.ModelSerializer):
#     count = serializers.IntegerField(read_only=True)
#
#     class Meta:
#         model = Collection
#         fields = ('id', 'count')
