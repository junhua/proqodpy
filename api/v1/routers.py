from rest_framework.routers import DefaultRouter

from myapp.courses.views import (
    CourseViewSet,
    AssessmentViewSet
)

router = DefaultRouter()

router.register(r'courses', CourseViewSet)
router.register(r'assessment', AssessmentViewSet)
