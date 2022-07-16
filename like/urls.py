from django.urls import path, include

from .views import LikeViewSet, PackageLikeCountViewSet, LikeCountRankViewSet

urlpatterns = [
    path('like/', LikeViewSet.as_view(), name=""),
    path('like/count/', PackageLikeCountViewSet.as_view()),
    path('like/rank/',LikeCountRankViewSet.as_view())
]