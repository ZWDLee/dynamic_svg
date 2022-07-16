from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status
from django.http import StreamingHttpResponse
import random
import json
import math
import datetime

from .serializers import SvgSerializer, SvgPackageSerializer, ShowEditPackageSerializer
from .models import Svg, SvgPackage
from collection.models import Collection
from like.models import Like
from oAuth.models import NewUser
from svg.permissions import IsOwnerOrReadOnly
from utils.pagination import CustomPagination
# Create your views here.



'''
1. svg详细信息
2. 更新、删除svg
'''
class SvgEditdViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Svg.objects.all()
    serializer_class = SvgSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)

'''
获取首页与访问用户的svgPackage
'''

class SvgPackageListViewSet(generics.ListAPIView):
    queryset = SvgPackage.objects.all()
    serializer_class = SvgPackageSerializer, SvgSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
    authentication_classes = []
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        uid = request.GET.get('uid')
        num = request.GET.get('num')
        page = int(request.GET.get('page'))
        size = int(request.GET.get('size'))
        if num is None:
            num = SvgPackage.objects.count() - 1
        if uid:
            author = get_object_or_404(NewUser, id=uid)
            data = SvgPackage.objects.filter(author=author).all()
            completeData = other_attr(num, data, author.username)
        else:
            data = SvgPackage.objects.all().order_by('-created_date')
            completeData = other_attr(num, data)

            for item in range(len(completeData)):
                if '自动' in completeData[item].package_tag.split(' '):
                    completeData[item].svgs = completeData[item].svgs[0: 1]
        total = math.ceil(completeData.count() / size)
        pagination = CustomPagination().paginate_queryset(completeData, request, view=self)
        serializer = SvgPackageSerializer(pagination, many=True)
        return CustomPagination().get_paginated_response(serializer.data, page, total, completeData.count())
        # return Response(svgPackageList.data)

def other_attr(num, data, author_name=None):
    if author_name:
        for item in range(len(data)):
            data[item].author_name = author_name
    else:
        for item in range(len(data)):
            data[item].author_name = data[item].author.username
    for item in range(len(data)):
        data[item].count = data[item].svg_set.count()
        data[item].date = data[item].created_date
        data[item].like_num = data[item].like_set.count()
        data[item].coll_num = data[item].collection_set.count()
        data[item].svgs = json.loads(
            json.dumps(SvgSerializer(data[item].svg_set.all().order_by('created_date')[:int(num)],
                                     many=True).data))
    return data


'''
随机图包数据
'''
class RandomPackageViewSet(generics.ListAPIView):
    queryset = SvgPackage
    serializer_class = SvgPackageSerializer
    permission_classes = []
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        # last = SvgPackage.objects.count()
        # first = random.randint(0, last)
        # if first > last - 8:
        #     first = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        # print(SvgPackage.objects.filter(package_tag__contains='自动'))
        # data = SvgPackage.objects.filter(package_tag__contains='自动')[first: first + 8]
        data = SvgPackage.objects.filter(package_tag__contains='自动')
        completeData = other_attr(6, data)
        packageList = SvgPackageSerializer(completeData, many=True)
        return Response(packageList.data)

'''
推荐图包
'''
class RecommendPackageViewSet(generics.ListAPIView):
    queryset = SvgPackage
    serializer_class = SvgPackageSerializer
    permission_classes = []
    authentication_classes = []

    def list(self, request, *args, **kwargs):

        data = SvgPackage.objects.filter(id=9)
        compliteData = other_attr(6, data)
        package = SvgPackageSerializer(compliteData, many=True)
        return Response(package.data)

'''
首页用户包列表
'''
class ShowEditPackageViewSet(generics.ListCreateAPIView):
    queryset = SvgPackage.objects.all()
    serializer_class = ShowEditPackageSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        page = int(request.GET.get('page'))
        size = int(request.GET.get('size'))
        uid = request.GET.get('uid')
        data = SvgPackage.objects.filter(author=uid).order_by('-created_date')
        for item in range(len(data)):
           data[item].like_num = data[item].like_set.count()
        total = math.ceil(data.count() / size)
        pagination = CustomPagination().paginate_queryset(data, request, view=self)
        serializer = ShowEditPackageSerializer(pagination, many=True)
        return CustomPagination().get_paginated_response(serializer.data, page, total, data.count())
        # return Response(packageList)

'''
获取图包信息
'''
class PackageViewSet(generics.ListAPIView,generics.UpdateAPIView):
    queryset = SvgPackage.objects.all()
    serializer_class = SvgPackageSerializer
    permission_classes = []
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        pid = request.GET.get('pid')
        data = SvgPackage.objects.filter(id=pid)
        if data.exists():
            for item in range(len(data)):
                data[item].author_name = data[item].author.username
                data[item].avatar = request.build_absolute_uri(data[item].author.avatar.url)
                data[item].date = data[item].created_date
                data[item].like_num = data[item].like_set.count()
                data[item].coll_num = data[item].collection_set.count()
            package = SvgPackageSerializer(data, many=True)
            return Response(package.data)
        else:
            return Response({'message': '不存在'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        pid = request.data.get('pid')
        instance = get_object_or_404(SvgPackage, id=pid)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)
        #
        # if getattr(instance, '_prefetched_objects_cache', None):
        #     # If 'prefetch_related' has been applied to a queryset, we need to
        #     # forcibly invalidate the prefetch cache on the instance.
        #     instance._prefetched_objects_cache = {}

        # return Response(serializer.data)
        return Response({'message': 1})

'''
修改图包信息
'''
class UpdateSvgPackageViewSet(generics.UpdateAPIView):
    queryset = SvgPackage.objects.all()
    serializer_class = SvgPackageSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

'''
新增图包
'''
import pdb
class AddSvgPackageViewSet(generics.CreateAPIView):
    queryset = SvgPackage.objects.all()
    serializer_class = SvgPackageSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        name = request.data['package_name']
        tag = request.data['package_tag']
        description = request.data['package_description']
        data = {
            'package_name': name,
            'package_tag': tag,
            'package_description': description,
            'author': request.user.id
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

'''
删除图包
'''
class SvgPackageDelViewSet(generics.DestroyAPIView):
    queryset = SvgPackage.objects.all()
    serializer_class = SvgPackageSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        pid = self.kwargs.get('pk')
        data = get_object_or_404(SvgPackage, id=pid)
        self.check_object_permissions(self.request, data)
        if data:
            data.delete()
            return Response({'message': '删除成功'}, status=status.HTTP_200_OK)
        return Response({'message': '删除失败'}, status=status.HTTP_404_NOT_FOUND)

'''
1.sid: svg_id uid: user_id
2.参数全为空：获取所有svg数据
3.sid为空，获取uid的所有svg
4.uid为空，获取sid的详细数据
5.创建新svg
'''
class SvgListViewSet(generics.ListCreateAPIView):
    queryset = Svg.objects.all()
    serializer_class = SvgSerializer
    permission_classes = []
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        pid = request.GET.get('pid')
        # uid = request.GET.get('uid')
        # params = {}
        # if pid:
        #     params['id'] = request.GET.get('pid')
        # if uid:
        #     params['author_id'] = request.GET.get('uid')
        # queryset = self.queryset.filter(**params)
        queryset = self.queryset.filter(package=pid)
        for item in range(len(queryset)):
            queryset[item].author_name = queryset[item].get_author().username
        svgList = SvgSerializer(queryset, many=True)
        return Response(svgList.data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        obj = get_object_or_404(SvgPackage, id=request.POST.get('package'))
        permission = self.check_object_permissions(self.request, obj)
        if permission:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
'''
下载
'''
class SvgDownloadViewSet(generics.ListAPIView):
    queryset = Svg.objects.all()
    serializer_class = SvgPackage
    permission_classes = []

    def list(self, request, *args, **kwargs):
        pid = request.GET.get('pid')
        svgExists = Svg.objects.filter(pk=pid).exists()
        if svgExists:
            svg = Svg.objects.get(pk=pid)
            isHTML = Svg.objects.filter(pk=pid, svg_code__contains="<style>").exists()
            if isHTML:
                response = StreamingHttpResponse('''<!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="UTF-8"><title>Document</title>
                        </head>
                        <body>
                            {}
                        </body>
                    </html>
                '''.format(svg.svg_code))
                filename = '{}.html'.format(svg.svg_name)
            else:
                response = StreamingHttpResponse(svg.svg_code, 'admin.svg')
                filename = '{}.svg'.format(svg.svg_name)
            response['Content-Type'] = 'application / octet - stream'
            response['COntent-Disposition'] = 'attachment;filename="{}"'.format(filename)
            return response
        return Response({"message": '图片id错误'}, status.HTTP_404_NOT_FOUND)
        # response = StreamingHttpResponse(svg.svg_code, 'admin.svg')
        # response['Content-Type'] = 'application / octet - stream'
        # response['Content-Disposition'] = 'attachment;filename="{}.svg"'.format(svg.svg_name)
        # return response

'''
上传
'''
class SvgUploadViewSet(generics.CreateAPIView):
    queryset = Svg.objects.all()
    serializer_class = SvgSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # obj = get_object_or_404(SvgPackage, id=request.POST.get('package'))
        # permission = self.check_object_permissions(self.request, obj)
        # if permission:
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

'''
删除svg
'''
class SvgDelViewSet(generics.DestroyAPIView):
    queryset = Svg.objects.all()
    serializer_class = SvgSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def destroy(self, request, *args, **kwargs):

        sid = self.kwargs.get('pk')
        data = get_object_or_404(Svg, id=sid)
        self.check_object_permissions(self.request, data)
        if data:
            data.delete()
            return Response({'message': '删除成功'}, status=status.HTTP_200_OK)
        return Response({'message': '删除失败'}, status=status.HTTP_404_NOT_FOUND)

'''
搜索
'''


'''
小程序端svgPackage
'''
class WxSvgPackageListViewSet(generics.ListAPIView):
    queryset = SvgPackage.objects.all()
    serializer_class = SvgPackageSerializer
    # permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)
    # authentication_classes = []
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        uid = request.GET.get('uid')
        # request.GET._mutable = True
        # request.GET['num'] = 1
        num = request.GET.get('num')
        page = int(request.GET.get('page'))
        size = int(request.GET.get('size'))
        if num is None:
            num = SvgPackage.objects.count() - 1
        if uid:
            author = get_object_or_404(NewUser, id=uid)
            data = SvgPackage.objects.filter(author=author).all()
            completeData = other_attr(num, data, author.username)
        else:
            data = SvgPackage.objects.filter(pure_svg_package=True).order_by('-created_date')
            completeData = other_attr(num, data)
        if request.user.is_authenticated:
            for item in range(len(completeData)):
                completeData[item].is_coll = Collection.objects.filter(
                    author=request.user,
                    package=completeData[item].id).exists()
                completeData[item].is_like = Like.objects.filter(uid=request.user, pid=completeData[item].id).exists()
        total = math.ceil(completeData.count() / size)
        pagination = CustomPagination().paginate_queryset(completeData, request, view=self)
        serializer = SvgPackageSerializer(pagination, many=True)
        return CustomPagination().get_paginated_response(serializer.data, page, total, completeData.count())











