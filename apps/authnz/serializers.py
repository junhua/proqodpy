from rest_framework import serializers
from .models import Student
from django.contrib.auth.models import User
# from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'Uid']


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = User
        fields = ['username', 'email','Uid']


class StudentRegistrationSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(
        max_length='55',
        source='student.student_id')

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
            User._meta.pk.name,
            'password',
            'student_id',
        )

        write_only_fields = (
            'password',
            'student_id',
        )

    def validate_student_id(self, value):
        # check if student_id is unique
        if Student.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("Student ID already registered.")
        return value

    def create(self, validated_data):
        student_id = validated_data['student']['student_id']

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'])

        profile = Student(user=user, student_id=student_id)
        profile.save()

        return user

class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'student_id')
