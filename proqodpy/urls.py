from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
# from apps.authnz.views import CustomRegistrationView, TeacherLoginView, get_user_info
from rest_framework.urlpatterns import format_suffix_patterns
# from apps.authnz import views


urlpatterns = [
    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Auth
    url(r'^auth/', include('authnz.urls')),

    # Api
    # url(r'^api/', include('apps.api.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
