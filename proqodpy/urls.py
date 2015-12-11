from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns


# from apps.courses.urls import router
from api.v1 import routers

urlpatterns = [
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Auth
    url(r'^auth/', include('authnz.urls')),

    # Api
    # url(r'^api/v1/courses/', include('apps.courses.urls'), name='courses'),
    url(r'^api/v1/', include(routers.router.urls)),

]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

