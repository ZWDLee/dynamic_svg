from rest_framework import serializers

from .models import Like, LikeCountRank

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'uid', 'pid', 'is_like')

class LikeCountRankSerialier(serializers.ModelSerializer):
    package_name = serializers.ReadOnlyField()
    package_description = serializers.ReadOnlyField()
    count = serializers.ReadOnlyField()
    date = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    package_tag = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField()
    author_name = serializers.ReadOnlyField()
    is_like = serializers.ReadOnlyField()
    is_coll = serializers.ReadOnlyField()
    like_num = serializers.ReadOnlyField()
    coll_num = serializers.ReadOnlyField()
    svgs = serializers.JSONField(read_only=True)

    class Meta:
        model = LikeCountRank
        fields = ('id', 'pid', 'package_name', 'package_description', 'count', 'date', 'package_tag', 'author',
                  'author_name', 'is_like', 'is_coll', 'like_num', 'coll_num', 'svgs')