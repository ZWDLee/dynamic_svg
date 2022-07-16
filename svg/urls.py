from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SvgListViewSet, SvgEditdViewSet, \
    SvgPackageListViewSet, RandomPackageViewSet, \
    RecommendPackageViewSet, ShowEditPackageViewSet, SvgDownloadViewSet, SvgUploadViewSet, \
    PackageViewSet, UpdateSvgPackageViewSet, SvgDelViewSet, AddSvgPackageViewSet, SvgPackageDelViewSet, \
    WxSvgPackageListViewSet


router = DefaultRouter()
# router.register('svg', SvgListViewSet),
# router.register('edit', SvgEditdSvgViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('svg/', SvgListViewSet.as_view()),
    path('svg/detail/<int:pk>', SvgEditdViewSet.as_view()),
    path('svg/package/', PackageViewSet.as_view()),
    path('svg/package/add/', AddSvgPackageViewSet.as_view()),
    path('svg/package/update/<int:pk>', UpdateSvgPackageViewSet.as_view()),
    path('svg/package/delete/<int:pk>', SvgPackageDelViewSet.as_view()),
    path('svg/package/list/', SvgPackageListViewSet.as_view()),
    path('wx/package/list/', WxSvgPackageListViewSet.as_view()),
    path('svg/package/guess/', RandomPackageViewSet.as_view()),
    path('svg/package/recommend/', RecommendPackageViewSet.as_view()),
    path('svg/package/user/all/', ShowEditPackageViewSet.as_view()),
    path('svg/download/', SvgDownloadViewSet.as_view()),
    path('svg/upload/', SvgUploadViewSet.as_view()),
    path('svg/delete/<int:pk>', SvgDelViewSet.as_view())
]
