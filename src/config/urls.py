"""car_salon_activities URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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


from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView as schema
from drf_spectacular.views import SpectacularRedocView as redoc
from drf_spectacular.views import SpectacularSwaggerView as swagger


api_v1_urls: tuple = (
    [
        path('auth/', include('jauth.api.v1.urls')),
        path('core/', include('core.api.v1.urls')),
        path('customer/', include('customer.api.v1.urls')),
        path('showroom/', include('showroom.api.v1.urls')),
        path('supplier/', include('supplier.api.v1.urls')),
    ],
    'v1',
)

urlpatterns: list = [
    path('api/v1/schema/', schema.as_view(api_version='v1'), name='schema'),
    path('api/v1/schema/swagger/', swagger.as_view(url_name='schema'), name='swagger'),
    path('api/v1/schema/redoc/', redoc.as_view(url_name='schema'), name='redoc'),
    path('api/v1/', include(api_v1_urls, namespace='v1')),
]


if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
