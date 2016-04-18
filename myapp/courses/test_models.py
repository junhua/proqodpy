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

        ProgrammingQuestion.objects.create(
            assessment=Assessment.objects.first(),
            number=2,
            type=0,
            description="",
            solution="",
            default_code="",
            language="r"
            code_signature="plus",
        )

        self.code = "def plus(a,b): return a+b"
        self.r_code = 'print("hi")'

    def test_unittest_can_execute(self):
        """ unit test can execute correctly """

        unittest = UnitTest.objects.first()
        result = unittest._execute_python(self.code)

        self.assertNotEqual(result, None)
        self.assertEqual(result[0], unittest.expected_output)

    def test_unittest_can_run(self):
        """ unit test can run """

        unittest = UnitTest.objects.first()
        result = unittest.run(self.code)

        self.assertEqual(type(result), dict)
        self.assertEqual(result.get("output"), unittest.expected_output)

    def test_r_unittest_can_run(self):
        """ R unit test can run """

        r_ut = UnitTest.objects.get(language="r")[0]
        result = unittest.execute(self.r_code)

        self.assertNotEqual(result, None)
        self.assertEqual(result.get("output"), unittest.expected_output)
