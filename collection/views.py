from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
import math

from .models import Collection, CollectionSvgList
from .serializers import CollectionSerializer, CollectionSvgListSerializer
from oAuth.models import NewUser
from svg.permissions import IsOwnerOrReadOnly
from utils.pagination import CustomPagination
# Create your views here.

'''
用户收藏列表
0: 用户收藏的
1: 用户创建的
'''
class CollectionViewSet(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request, *args, **kwargs):
        sign = int(request.GET.get('sign'))
        page = int(request.GET.get('page'))
        size = int(request.GET.get('size'))
        if request.user.is_authenticated is False:
            return Response({'msg': '请登录'}, status.HTTP_401_UNAUTHORIZED)
        if bool(sign):
            data = Collection.objects.filter(author=request.user, package__isnull=True).order_by('-created_date')
        else:
            data = Collection.objects.filter(author=request.user, package__isnull=False).order_by('-created_date')
        total = math.ceil(data.count() / size)
        pagination = CustomPagination().paginate_queryset(data, request, view=self)
        serializer = CollectionSerializer(pagination, many=True)
        return CustomPagination().get_paginated_response(serializer.data, page, total, data.count())
        # serializer = CollectionSerializer(data, many=True)
        # return Response(serializer.data)
'''
添加新收藏夹
'''
class CreateCollectionViewSet(generics.CreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def create(self, request, *args, **kwargs):
        author = int(request.data.get('author'))
        package = int(request.data.get('package'))
        if request.user.is_authenticated:
            exists = Collection.objects.filter(author=author, package=package).exists()
            if exists:
                collRecord = Collection.objects.get(author=author, package=package)
                if collRecord.is_coll == 1:
                    collRecord.is_coll = 0
                    collRecord.save()
                    result = -1
                else:
                    collRecord.is_coll = 1
                    collRecord.save()
                    result = 1
                return Response({'result': result})
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({'msg': '无权限'}, status.HTTP_403_FORBIDDEN)

'''
修改收藏夹
'''
class EditCollectionViewSet(generics.UpdateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

'''
删除收藏夹
'''
class DelColletionViewSet(generics.DestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


'''
非原图包收藏夹下的svg列表
'''
class CollectionSvgListViewSet(generics.ListAPIView):
    queryset = CollectionSvgList.objects.all()
    serializer_class = CollectionSvgListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def list(self, request, *args, **kwargs):
        cid = request.GET.get('collection')
        data = CollectionSvgList.objects.filter(collection=cid, collection__author=request.user, is_coll=1)
        for item in range(len(data)):
            data[item].svg_code = data[item].svg.svg_code
            data[item].svg_name = data[item].svg.svg_name
            data[item].coll_name = data[item].collection.coll_name
        serializer = CollectionSvgListSerializer(data, many=True)
        return Response(serializer.data)
'''
收藏svg
'''
class CollectionSvgViewSet(generics.CreateAPIView):
    queryset = CollectionSvgList.objects.all()
    serializer_class = CollectionSvgListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        cid = request.data.get('collection')
        sid = request.data.get('svg')
        author = get_object_or_404(Collection, pk=cid).author
        if author != request.user:
            return Response({'msg': '无权限'}, status.HTTP_403_FORBIDDEN)
        isExists = CollectionSvgList.objects.filter(
            pk=sid, collection=cid).exists()
        if isExists:
            result = CollectionSvgList.objects.get(pk=sid, collection=cid)
            result.is_coll = 0 if bool(result.is_coll) else 1
            result.save()
            return Response({'msg': ''})
        return Response({})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

'''
图包被收藏总数
'''
class PackageCollectionCountViewSet(generics.ListAPIView):
    queryset = Collection.objects.all()
    # serializer_class = CollectionCountSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated is False:
            return Response({'msg': '请登录'}, status.HTTP_401_UNAUTHORIZED)
        data = Collection.objects.filter(package__author=request.user).count()
        return Response({'count': data}, status.HTTP_200_OK)

'''
微信端收藏列表
'''
class WxCollectionViewSet(generics.ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def list(self, request, *args, **kwargs):
        sign = int(request.GET.get('sign'))
        if request.user.is_authenticated is False:
            return Response({'msg': '请登录'}, status.HTTP_401_UNAUTHORIZED)
        if bool(sign):
            data = Collection.objects.filter(author=request.user, package__isnull=True).order_by('-created_date')
        else:
            data = Collection.objects.filter(author=request.user, package__isnull=False).order_by('-created_date')
        serializer = CollectionSerializer(data, many=True)
        return Response(serializer.data)







