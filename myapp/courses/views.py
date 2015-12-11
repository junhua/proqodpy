
from .serializers import CourseSerializer
from .models import Course
from rest_framework import viewsets, authentication, permissions, filters

class DefaultsMixin(object):
	""" Default settings for view auth, permissions, filtering and pagination """
	authentication_classes = (
			authentication.BasicAuthentication,
			authentication.TokenAuthentication,
		)
	permission_classes = (
			permissions.IsAuthenticated,
		)
	paginate_by = 25
	paginate_by_param = "school"
	filter_backends = (
			filters.DjangoFilterBackend,
			filters.SearchFilter,
			filters.OrderingFilter,
		)

class CourseViewSet(DefaultsMixin, viewsets.ModelViewSet):
	""" API endpoint for listing and creating courses """
	queryset = Course.objects.order_by('date_created')
	serializer_class = CourseSerializer

