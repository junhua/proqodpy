from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
# from apps.authnz.views import CustomRegistrationView, TeacherLoginView, get_user_info
from rest_framework.urlpatterns import format_suffix_patterns
# from apps.authnz import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'proqodpy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    # url(r'^auth/me/', views.get_user_info),
    # url(r'^register/$', CustomRegistrationView.as_view()),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)