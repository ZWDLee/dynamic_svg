"""dynamic_svg_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi


scheme_view = get_schema_view(
    openapi.Info(
        title='Books API',
        default_version='v1',
        description='books',
        terms_of_service='http://localhost:8000',
        contact=openapi.Contact('943318968@qq.com'),
        license=openapi.License(name="Ip")
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('doc/', scheme_view.with_ui('swagger', cache_timeout=0), name='scheme-swagger-ui'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('oAuth.urls')),
    path('api/', include('svg.urls')),
    path('api/', include('like.urls')),
    path('api/', include('collection.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
