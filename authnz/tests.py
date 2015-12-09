from django.test import TestCase
import djet

from django.contrib.auth import get_user_model, user_logged_in, user_login_failed, user_logged_out
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test.utils import override_settings
from djet import assertions, utils, restframework
from rest_framework import status


# Create your tests here.

def create_user(**kwargs):
    data = {
        'sid': '1000001',
        'password': 'secret',
        'email': 'john@proqod.com',
    }
    data.update(kwargs)
    user = get_user_model().objects.create_user(**data)
    user.raw_password = data['password']
    return user