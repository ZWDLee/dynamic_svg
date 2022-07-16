from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from django.http import HttpResponse

from .serializers import NewUserSerializer, NewUserSignupSerializer, UploadAvatarSerializer
from .models import NewUser
from .permissions import IsOwerOrFobbiden
# Create your views here.

class UserInfoViewSet(viewsets.ViewSet):
    queryset = NewUser.objects.all().order_by('-date_joined')
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        user = NewUser.objects.filter(id=request.user.id)
        user_info = NewUserSerializer(user, many=True, context={request: 'request'})
        return Response(user_info.data)

class UserRegisterViewSet(generics.CreateAPIView):
    queryset = NewUser.objects.all()
    serializer_class = NewUserSignupSerializer
    permission_classes = []
    authentication_classes = []

class UserResetPwdViewSet(generics.UpdateAPIView):
    queryset = NewUser.objects.all()
    permission_classes = []
    authentication_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwerOrFobbiden]

    def partial_update(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = NewUser.objects.get(username=username, email=email)
        except NewUser.DoesNotExist:
            return Response({'message': '用户名与邮箱不匹配，请联系管理员'}, status=status.HTTP_404_NOT_FOUND)
        user.set_password(password)
        user.save()
        return Response({'message': '修改成功'})

# class UploadAvatarViewSet(generics.UpdateAPIView):
#     queryset = NewUser.objects.all()
#     serializer_class = UploadAvatarSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwerOrFobbiden]
#
#     def update(self, request, *args, **kwargs):
#         new_avatar = request.FILES.get('avatar')
#         user = NewUser.objects.get(pk=request.user.id)
#         user.avatar = new_avatar
#         user.save()
#         return Response({'message': '修改成功'}, status.HTTP_200_OK)






