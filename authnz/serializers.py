from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import *
from myapp.courses.models import *


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    cohort_classes_students = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    cohort_classes_teachers = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User._meta.pk.name,
            User.USERNAME_FIELD,
            'cohort_classes_students',
            'cohort_classes_teachers',
        )
        read_only_fields = (
            User.USERNAME_FIELD,
        )
