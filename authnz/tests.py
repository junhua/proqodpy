from django.test import TestCase
import djet

from django.contrib.auth import get_user_model, user_logged_in, user_login_failed, user_logged_out
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test.utils import override_settings
from djet import assertions, utils, restframework
from rest_framework import status
from django.conf import settings
from djoser import views
import djoser
# Create your tests here.

# def create_user(**kwargs):
#     data = {
#         'sid': '1000001',
#         'password': 'secret',
#         'email': 'john@proqod.com',
#     }
#     data.update(kwargs)
#     user = get_user_model().objects.create_user(**data)
#     user.raw_password = data['password']
#     return user

# class RegistrationViewTest(restframework.APIViewTestCase,
#                            assertions.StatusCodeAssertionsMixin,
#                            assertions.EmailAssertionsMixin,
#                            assertions.InstanceAssertionsMixin):
#     view_class = djoser.views.RegistrationView

#     def test_post_should_create_user_without_login(self):
#         data = {
#             'username': 'john',
#             'password': 'secret',
#             'csrftoken': 'asdf',
#         }
#         request = self.factory.post(data=data)

#         response = self.view(request)

#         self.assert_status_equal(response, status.HTTP_201_CREATED)
#         self.assertTrue('password' not in response.data)
#         self.assert_instance_exists(get_user_model(), username=data['username'])
#         user = get_user_model().objects.get(username=data['username'])
#         self.assertTrue(user.check_password(data['password']))

#     @override_settings(DJOSER=dict(settings.DJOSER, **{'SEND_ACTIVATION_EMAIL': True}))
#     def test_post_should_create_user_with_login_and_send_activation_email(self):
#         data = {
#             'username': 'john',
#             'email': 'john@beatles.com',
#             'password': 'secret',
#         }
#         request = self.factory.post(data=data)

#         response = self.view(request)

#         self.assert_status_equal(response, status.HTTP_201_CREATED)
#         self.assert_instance_exists(get_user_model(), username=data['username'])
#         self.assert_emails_in_mailbox(1)
#         self.assert_email_exists(to=[data['email']])

#     def test_post_should_not_create_new_user_if_username_exists(self):
#         create_user(username='john')
#         data = {
#             'username': 'john',
#             'password': 'secret',
#             'csrftoken': 'asdf',
#         }
#         request = self.factory.post(data=data)

#         response = self.view(request)

#         self.assert_status_equal(response, status.HTTP_400_BAD_REQUEST)
