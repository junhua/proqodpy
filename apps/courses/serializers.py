from rest_framework import serializers
from .models import Course
from django.contrib.auth.models import User

class CourseSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Course
		fields = ('school', 'courseCode', 'title', 'department', 'description', 
				'programming_language', 'startDate', 'endDate')
		
