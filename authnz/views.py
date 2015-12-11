from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
# from rest_framework.response import Response
from rest_framework import permissions, generics
from djoser import signals, settings, utils, serializers

# from .serializers import UserRegistrationSerializer

User = get_user_model()
