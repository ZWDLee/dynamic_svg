from rest_framework import serializers

from .models import Svg, SvgPackage

class SvgSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True, max_length=32)
    num = serializers.IntegerField(read_only=True)

    class Meta:
        model = Svg
        fields = ('id', 'svg_name', 'svg_code', 'pure_svg', 'package', 'author', 'author_name', 'num')

class SvgPackageSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True, max_length=20)
    avatar = serializers.ReadOnlyField()
    svgs = serializers.JSONField(read_only=True)
    date = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    count = serializers.CharField(read_only=True)
    is_like = serializers.ReadOnlyField()
    is_coll = serializers.ReadOnlyField()
    like_num = serializers.ReadOnlyField()
    coll_num = serializers.ReadOnlyField()

    class Meta:
        model = SvgPackage
        fields = ('id', 'package_name', 'avatar', 'package_description', 'count', 'date',
                  'package_tag', 'author', 'author_name', 'is_like', 'is_coll', 'like_num', 'coll_num', 'svgs')

class ShowEditPackageSerializer(serializers.ModelSerializer):
    like_num = serializers.ReadOnlyField()

    class Meta:
        model = SvgPackage
        fields = ('id', 'package_name', 'package_description', 'package_tag', 'author', 'like_num')