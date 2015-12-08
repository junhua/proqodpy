from django.conf.urls import *
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.DefaultRouter(trailing_slash=False)
# router.register(r'courses',views.CourseViewSet)

urlpatterns = [url(r'^api/', include(router.urls)),]
