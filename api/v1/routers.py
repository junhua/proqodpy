from rest_framework.routers import DefaultRouter

from myapp.courses.views import CourseViewSet

router = DefaultRouter()

router.register(r'courses', CourseViewSet)
