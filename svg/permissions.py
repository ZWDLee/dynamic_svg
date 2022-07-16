from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限只允许对象的所有者编辑它。
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author.id == request.user.id

    # def has_permission(self, request, view):
    #     if request.user.has_perm('app名.权限标识'):
    #         return True
    #     else:
    #         print('aaa')
    #         return False