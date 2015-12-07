from django.shortcuts import render, render_to_response
from .serializers import CourseSerializer
from .models import Course
from rest_framework.permissions import IsAuthenticated
# from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import detail_route, list_route
from django.template import RequestContext
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# def index(request):
#   return render_to_response('courses.html', RequestContext(request))

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # allowed_methods = ('get', 'post', 'put', 'delete','patch')

    # permission_classes = (IsOwnerOrReadOnly,)
    permission_classes = (IsAuthenticated,)

    # def list(self, request):
    #     ...

    
    

        # Course.object.create()

    # def retrieve(self, request, pk=None):
    #     ...
    # def update(self, request, pk=None):
    #     ...
    # def destroy(self, request, pk=None):
    #     ...

    def pre_save(self,obj):
        obj.owner = self.request.user

    @list_route(methods=['post'])
    def create_course(self, request):
        course = Course.object.create(data=request.data)
        return course

    def get_serializer_class(self):
        return CourseSerializer