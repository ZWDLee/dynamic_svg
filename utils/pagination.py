from rest_framework.pagination import PageNumberPagination, Response
from rest_framework.views import status

class CustomPagination(PageNumberPagination):
   page_size = 9
   page_size_query_param = 'size'
   max_page_size = 18
   page_query_param = 'page'

   def get_paginated_response(self, data, page, total, count=None):
      if page > total:
         return Response({'msg': '已经是最后一页', 'code': '0'}, status=status.HTTP_204_NO_CONTENT)
      if count is None:
         return Response({
            'data': data,
            'page': page,
            'total': total
         })
      else:
         return Response({
            'data': data,
            'page': page,
            'total': total,
            'count': count
         })
