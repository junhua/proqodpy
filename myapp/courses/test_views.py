# import json
# from django.core.urlresolvers import reverse
# from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from .models import Course, Assessment
from authnz.models import ProqodUser

# from .views import CourseViewSet


class CourseViewsTests (APITestCase):

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

    def test_create_course(self):
        factory = APIRequestFactory()
        data = {
            'course_batch': "test_batch",
            'course_code': "CS101",
            'school': "ProQod Institute",
            'department': "ProQod Dept",
            'title': "Intro to CS",
            'description': "Introduction course to computer science",
            'programming_language': "Python",
            'start_date': "2015-12-01",
            'end_date': "2016-01-01",
        }

        # response = factory.post("/api/v1/course-list", data)
        response = self.client.post("/api/v1/course-list", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(Course.objects.get().course_batch, data.course_batch)

    def test_read_course(self):
        factory = APIRequestFactory()
        # response = factory.get("/api/v1/course/1/")
        response = self.client.get("/api/v1/course/1", format="json")

        self.assertEqual(
            response.data, {'id': 1, 'course_batch': 'test_batch'})

    def test_update_course(self):

        factory = APIRequestFactory()
        # response = factory.put('/notes/1/', {'course_code': 'CS102'})
        response = self.client.put(
            "/api/v1/course/1/", {'course_code': 'CS102'}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get().course_code, 'CS102')
        factory.put('/notes/1/', {'course_code': 'CS101'})

    def test_delete_course(self):

        factory = APIRequestFactory()
        # response = factory.put('/notes/1/', {'course_code': 'CS102'})
        response = self.client.delete(
            "/api/v1/course/1/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.get().course_code, 'CS102')
        factory.put('/notes/1/', {'course_code': 'CS101'})
