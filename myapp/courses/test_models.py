from django.test import TestCase
from datetime import datetime
from models import (UnitTest, ProgrammingQuestion, Assessment)


class UnittestTestCase(TestCase):

    def setUp(self):
        Assessment.objects.create(
            type=0,
            label=1,
            description="",
            start_datetime=datetime.now(),
            end_datetime=datetime.now(),
        )

        ProgrammingQuestion.objects.create(
            assessment=Assessment.objects.first(),
            number=1,
            type=0,
            description="",
            solution="",
            default_code="",
            code_signature="plus",
        )

        UnitTest.objects.create(
            visibility=0,
            type=0,
            language=0,
            test_content='',
            inputs=[1, 2],
            expected_output=3,
            question=ProgrammingQuestion.objects.first(),
        )
        self.code = "def plus(a,b): return a+b"

    def test_unittest_can_run(self):
        """ unit test can run """
        unittest = UnitTest.objects.first()

        result = unittest.run(self.code)
        self.assertEqual(type(result), dict)

    def test_unittest_can_execute(self):
        """ unit test can execute correctly """
        unittest = UnitTest.objects.first()

        result = unittest.execute(self.code)

        self.assertNotEqual(result, None)
