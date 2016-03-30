from django.conf.urls import url, include

urlpatterns = [
    url(r'^jwt-login/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^', include('djoser.urls.authtoken')),
]
