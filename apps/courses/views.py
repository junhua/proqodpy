
from .serializers import CourseSerializer
from .models import Course
from rest_framework import viewsets
from rest_framework import authentication, permissions

class DefaultsMixin(object):
	""" Default settings for view auth, permissions, filtering and pagination """
	authentication_classes = (
			authentication.BasicAuthentication,
			authentication.TokenAuthentication,
		)
	permission_classes = (
			permissions.IsAuthenticated,
		)
	paginated_by = 25


class CourseViewSet(DefaultsMixin, viewsets.ModelViewSet):
	""" API endpoint for listing and creating courses """
	queryset = Course.objects.order_by('date_created')
	serializer_class = CourseSerializer


# from django.shortcuts import render, render_to_response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.generics import ListCreateAPIView
# from rest_framework.generics import RetrieveUpdateDestroyAPIView
										

# class CourseCreateReadView(ListCreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     permission_classes = (IsAuthenticated,)

# class CourseReadUpdateDeleteView(RetrieveUpdateDestroyAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer
#     permission_classes = (IsAuthenticated,)
