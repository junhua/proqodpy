from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):

    participants = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'course_batch',
            'course_code',
            'school',
            'department',
            'title',
            'description',
            'programming_language',
            'start_date',
            'end_date',
            'participants',
        )
        search_fields = ('school', )
        ordering_fields = ('school', 'department', 'date_created', )
