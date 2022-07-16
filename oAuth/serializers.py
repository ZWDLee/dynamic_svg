from rest_framework import serializers, validators
from .models import NewUser

class NewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('id', 'username', 'email', 'avatar')

class NewUserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('username', 'email', 'password')
        extra_kwarge = {
            'username': {
                'help_text': '用户名',
                'min_length': 6,
                'max_length': 32,
                'error_messages': {
                    'min_length': '用户名为6~32个字符',
                    'max_length': '用户名为6~32个字符'
                }
            },
            'email': {
                'help_text': '邮箱',
                'required': True,
                'write_only': True,
                'validators': [validators.UniqueValidator(queryset=NewUser.objects.all(), message='此邮箱已被注册')]
            },
            'password': {
                'help_text': '密码',
                'write_only': True,
                'min_length': 6,
                'max_length': 24,
                'error_messages': {
                    'max_length': '密码为8~24个字符',
                    'min_length': '密码为8~24个字符'
                }
            }
        }

    def create(self, validated_data):
        user = NewUser.objects.create_user(**validated_data)
        return user

class UploadAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('avatar', )