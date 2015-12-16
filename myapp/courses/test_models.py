import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
from .models import Course, Assessment
from authnz.models import ProqodUser

from .views import CourseViewSet


class CourseModelTests (APITestCase):

    def setUp(self):

        Course.objects.get_or_create(
            course_batch="test_batch",
            course_code="CS101",
            school="ProQod Institute",
            department="ProQod Dept",
            title="Intro to CS",
            description="Introduction course to computer science",
            programming_language="Python",
            start_date="2015-12-01",
            end_date="2016-01-01",
        )

        ProqodUser.objects.create_user(
            email="test1@proqod.com",
            sid="10001",
            password="pw",

        )

        ProqodUser.objects.create_user(
            email="test2@proqod.com",
            sid="10002",
            password="pw"
        )

        ProqodUser.objects.create_user(
            email="test3@proqod.com",
            sid="10003",
            password="pw"
        )

    # def test_create_course(self):

    #     self.assertEqual()
