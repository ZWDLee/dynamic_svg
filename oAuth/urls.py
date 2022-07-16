from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserRegisterViewSet, UserInfoViewSet, UserResetPwdViewSet

router = DefaultRouter()
router.register('userInfo', UserInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/register/', UserRegisterViewSet.as_view()),
    path('user/reset/', UserResetPwdViewSet.as_view()),
    # path('user/update/', UploadAvatarViewSet.as_view()),
]