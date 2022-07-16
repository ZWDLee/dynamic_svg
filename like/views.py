from rest_framework import mixins, generics, permissions, status
from rest_framework.response import Response
import json
import math
from django.utils import timezone
from django.http import HttpResponse

from .models import Like, LikeCountRank
from .serialisers import LikeSerializer, LikeCountRankSerialier
from svg.serializers import SvgSerializer
from svg.models import SvgPackage
from oAuth.models import NewUser
from utils.throttles import LikeThrottle
from utils.pagination import CustomPagination
# Create your views here.

#
class LikeViewSet(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    throttle_classes = [LikeThrottle]

    def list(self, request, *args, **kwargs):
        pid = request.GET.get('pid')
        uid = request.GET.get('uid')
        like = Like.objects.filter(pid=pid, uid=uid)
        if len(like) == 0:
            Like.objects.create(
                uid=NewUser.objects.get(pk=uid),
                pid=SvgPackage.objects.get(pk=pid),
                is_like=1
            )
            result = 1
        else:
            likeRecord = Like.objects.get(pid=pid, uid=uid)
            if bool(likeRecord.is_like):
                likeRecord.is_like = 0
                likeRecord.save()
                result = -1
            else:
                likeRecord.is_like = 1
                likeRecord.save()
                result = 1
        isExists = LikeCountRank.objects.filter(pid=pid).exists()
        if isExists:
            data = LikeCountRank.objects.get(pid=pid)
            data.range_count = data.range_count + result
            data.save()
        else:
            data = LikeCountRank(pid=SvgPackage.objects.get(pk=pid), range_count=1 if result == 1 else 0)
            data.save()
        return Response({'result': result})

    # def create(self, request, *args, **kwargs):
    #     uid = request.POST.get('uid')
    #     pid = request.POST.get('pid')
    #     if uid is None:
    #         return Response({'message': '未登录，没有权限'}, status=status.HTTP_403_FORBIDDEN)
    #     likeRecord = Like.objects.filter(uid=uid, pid=pid)
    #     if likeRecord:
    #         if likeRecord[0].is_like == 1:
    #             likeRecord[0].is_like = 0
    #         else:
    #             likeRecord[0].is_like = 1
    #         likeRecord[0].save()
    #         return Response(LikeSerializer(likeRecord[0]).data)
    #     else:
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PackageLikeCountViewSet(generics.ListAPIView):
    queryset = Like.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated is False:
            return Response({'msg': '请登录'}, status.HTTP_401_UNAUTHORIZED)
        data = Like.objects.filter(pid__author=request.user).count()
        return Response({'count': data}, status.HTTP_200_OK)

class LikeCountRankViewSet(generics.ListAPIView):
    queryset = LikeCountRank.objects.all()
    serializer_class = LikeCountRankSerialier
    permission_classes = []
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        num = int(request.GET.get('num'))
        page = int(request.GET.get('page'))
        size = int(request.GET.get('size'))
        now = timezone.now()
        data = self.queryset.filter(created_data__month=now.month, pid__pure_svg_package=True)
        print(data)
        for item in range(len(data)):
            data[item].package_name = data[item].pid.package_name
            data[item].package_description = data[item].pid.package_description
            data[item].package_tag = data[item].pid.package_tag
            data[item].author = data[item].pid.author.id
            data[item].author_name = data[item].pid.author.username
            data[item].count = data[item].pid.svg_set.count()
            data[item].date = data[item].pid.created_date
            data[item].like_num = data[item].pid.like_set.filter(is_like=1).count()
            data[item].coll_num = data[item].pid.collection_set.count()
            data[item].svgs = json.loads(
                json.dumps(SvgSerializer(data[item].pid.svg_set.all().order_by('created_date')[:num],
                                         many=True).data))
            if request.user.is_authenticated:
                data[item].is_like = Like.objects.filter(uid=request.user, pid=data[item].pid, is_like=1).exists()
        total = math.ceil(data.count() / size)
        pagination = CustomPagination().paginate_queryset(data, request, view=self)
        serializer = LikeCountRankSerialier(pagination, many=True)
        return CustomPagination().get_paginated_response(serializer.data, page, total, data.count())



