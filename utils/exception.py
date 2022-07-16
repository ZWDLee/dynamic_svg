from rest_framework.views import exception_handler, Response
from rest_framework import status

def custom_exception_handle(exc, context):
    response = exception_handler(exc, context)
    msg = exc.__str__()
    e_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    if msg == 'No active account found with the given credentials':
        msg = '用户名或密码不正确'
        e_status = status.HTTP_401_UNAUTHORIZED
    if response is None:
        return Response({'message': '错误：{}'.format(msg)}, status=e_status,
                        exception=True)
    else:
        return Response({'message': '错误：{}'.format(msg)}, status=response.status_code, exception=True)
