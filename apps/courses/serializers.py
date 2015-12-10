from rest_framework import serializers
from .models import Course
from django.contrib.auth.models import User

class CourseSerializer(serializers.ModelSerializer):
    students = serializers.StringRelatedField(many=True)
    teachers = serializers.StringRelatedField(many=True)


	class Meta:
		model = Course
		fields = ('course_batch',
					'course_code',
					'school',
					'department',
					'title',
					'description',
					'programming_language',
					'start_date',
					'end_date',
					'teachers',
					'students',)
