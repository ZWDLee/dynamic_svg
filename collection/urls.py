from django.urls import path

from .views import CollectionViewSet, CreateCollectionViewSet, EditCollectionViewSet, DelColletionViewSet, \
    CollectionSvgViewSet, CollectionSvgListViewSet, PackageCollectionCountViewSet, WxCollectionViewSet

urlpatterns = [
    path('collection/list/', CollectionViewSet.as_view()),
    path('wx/collection/list/', WxCollectionViewSet.as_view()),
    path('collection/add/', CreateCollectionViewSet.as_view()),
    path('collection/edit/<int:pk>', EditCollectionViewSet.as_view()),
    path('collection/del/<int:pk>', DelColletionViewSet.as_view()),
    path('collection/svg/list/', CollectionSvgListViewSet.as_view()),
    path('collection/svg/add/', CollectionSvgViewSet.as_view()),
    path('collection/count/', PackageCollectionCountViewSet.as_view()),
]