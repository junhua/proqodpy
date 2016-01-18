from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import *
from .models import *
from myapp.courses.models import UnitTest
from myapp.analytics.models import PerformanceReport
import sys


class DefaultsMixin(object):

    """ 
    Default settings for view auth, permissions,
    filtering and pagination
    """
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25
    paginate_by_param = "school"
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class UnittestEntryViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = UnittestEntry.objects.all()
    serializer_class = UnittestEntrySerializer


class CodeSubmissionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Code Submission """
    queryset = CodeSubmission.objects.order_by('date_created')
    serializer_class = CodeSubmissionSerializer
    filter_fields = ['question', 'created_by']

    def create(self, request):
        """
        Override default POST method:
        1. create Submission
        2. create Performance report

        """

        data = request.data

        try:
            user = request.user
            code = data.get('code', None)
            question = ProgrammingQuestion.objects.get(
                id=data.get('question', None))
        except:
            return Response(
                {"message": "Required user, code and question params"},
                status=400
            )

        # SCORE

        unittests = UnitTest.objects.filter(question=question)
        ut_entries = []
        ut_passed = 0
        total_time = 0.0

        for unittest in unittests:
            test = unittest.run(code)

            data = {
                'visibility': unittest.visibility,
                'inputs': ", ".join(unittest.inputs) if unittest.visibility else "-",
                'expected_output': unittest.expected_output if unittest.visibility else "-",
                'actual_output': test.get('output', test.get('error', None)) if unittest.visibility else "-",
                'is_correct': test.get('pass', False),
            }
            if data['is_correct']:
                ut_passed += 1
                total_time += test['time']

            ut_entry = UnittestEntrySerializer(data=data)
            if ut_entry.is_valid():
                ut_entry.save()
                ute = UnittestEntry.objects.get(id=ut_entry.data['id'])
                ut_entries += [ute]
            else:
                return Response(ut_entry.errors, 400)

        # PERFORMANCE REPORT (To be edited)
        complexity = -1
        memory = -1
        # time = PerformanceReport.objects.time_exec(code)
        time = total_time / ut_passed if ut_passed>0 else -2
        correctness = round((ut_passed + 0.0) / len(ut_entries), 2)
        size = len(code)

        report = PerformanceReport(
            complexity=complexity,
            memory=memory,
            time=time,
            correctness=correctness,
            size=size
        )

        try:
            report.save()
            print report.id
        except:
            return Response(
                {"message": "Failed to create performance report"},
                status=404
            )

        data = {
            'created_by': user.id,
            'code': code,
            'question': question.id,
            'type': 0,
            'unittest_entries': [entry.id for entry in ut_entries],
            'performance_report': report.id
        }

        # subm = CodeSubmission(
        #     created_by=user,
        #     code=code,
        #     question=question,
        #     performance_report=report,
        #     type=0,
        #     unittest_entries=ut_entries
        # )
        # print subm.id
        subm = CodeSubmissionCreateSerializer(data=data)

        if subm.is_valid():
            subm.save()

            cs = CodeSubmission.objects.get(id=subm.data["id"])
            data = CodeSubmissionSerializer(cs).data

            return Response(data, status=201)
        else:
            return Response(subm.errors, status=400)


class BlankSubmissionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Code Submission """

    queryset = BlankSubmission.objects.order_by('date_created')
    serializer_class = BlankSubmissionSerializer
    filter_fields = ['question', 'created_by']

    def create(self, request):
        """
        Override default POST method to create BlankSubmission

        """
        data = request.data

        question = get_object_or_404(BlankQuestion, pk=data.get('question'))
        solutions = BlankSolution.objects.filter(
            question=question).order_by('seq')
        blanks = data.get('blanks', None)

        # Check submitted blanks
        # blanks should not be more than #solutions
        # if $blanks less than #solutions, fill list with False

        if len(blanks) > len(solutions):
            return Response({"Detail": "too many blanks"}, status=404)

        checks = [str(blanks[i]) == solutions[i].content
                  for i in xrange(len(blanks))]
        checks += [False for _ in xrange(len(solutions) - len(blanks))]

        data['evaluation'] = checks
        data['type'] = 2

        subm_serializer = BlankSubmissionSerializer(data=data)
        if subm_serializer.is_valid():
            subm_serializer.save()
            return Response(subm_serializer.data, status=201)
        else:
            return Response(subm_serializer.errors, status=400)


class McqSubmissionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Code Submission """
    queryset = McqSubmission.objects.order_by('date_created')
    serializer_class = McqSubmissionSerializer
    filter_fields = ['question', 'created_by']


class CheckoffSubmissionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Code Submission """
    queryset = CheckoffSubmission.objects.order_by('date_created')
    serializer_class = CheckoffSubmissionSerializer
    filter_fields = ['question', 'created_by']


class McqProgressViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Mcq Progress """
    queryset = McqProgress.objects.all()
    serializer_class = McqProgressSerializer
    filter_fields = ['question', 'student']

    # def create(self, request):
    #     """
    #     Parameters: question(id), answer
    #     """
    #     data = request.data
    #     student = request.user
    #     question_id = data.get('question', None)

    #     if not student or not question_id:
    #         return Response(
    #             {"message": "student or question empty"},
    #             status=404
    #         )

    #     try:

    #         question = Mcq.objects.get(id=question_id)
    #         progress, _ = McqProgress.objects.update_or_create(
    #             student=student,
    #             question=question,
    #             defaults={
    #                 'choice': MultipleChoice.objects.get(id=data.get('choice', None))
    #             }
    #         )

    #         return Response(McqProgressSerializer(progress).data, status=200)
    #     except ValueError as ve:
    #         return Response({"error": str(ve)}, status=400)
    # return Response({"error": str(sys.exc_info()[0])}, status=400)

    #     return Response({"error": "oops..."}, status=400)


class BlankQuestionProgressViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Blank question progress """
    queryset = BlankQuestionProgress.objects.all()
    serializer_class = BlankQuestionProgressSerializer
    filter_fields = ['question', 'student']

    # def create(self, request):
    #     """
    #     Parameters: question(id), answer_last_saved
    #     """
    #     data = request.data
    #     student = request.user
    #     question_id = data.get('question', None)

    #     if not student or not question_id:
    # return Response({"message": "student or question empty"}, status=404)

    #     try:

    #         question = BlankQuestion.objects.get(id=question_id)
    #         progress, _ = BlankQuestionProgress.objects.update_or_create(
    #             student=student,
    #             question=question,
    #             defaults={
    #                 'answer_last_saved': data.get('answer_last_saved', None)
    #             }
    #         )

    #         return Response(BlankQuestionProgressSerializer(progress).data, status=200)
    #     except ValueError as ve:
    #         return Response({"error": str(ve)}, status=400)
    # return Response({"error": str(sys.exc_info()[0])}, status=400)

    #     return Response({"error": "oops..."}, status=400)


class ProgrammingQuestionProgressViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Programming Question Progress """
    queryset = ProgrammingQuestionProgress.objects.all()
    serializer_class = ProgrammingQuestionProgressSerializer
    filter_fields = ['question', 'student']

    # def create(self, request):
    #     """
    #     Parameters: question(id), code
    #     """
    #     data = request.data
    #     student = request.user
    #     question_id = data.get('question', None)

    #     if not student or not question_id:
    #         return Response(
    #             {"message": "student or question empty"}, status=404)

    #     try:
    #         question = ProgrammingQuestion.objects.get(id=question_id)
    #         progress, _ = ProgrammingQuestionProgress.objects.update_or_create(
    #             student=student,
    #             question=question,
    #             defaults={
    #                 'answer_last_saved': data.get('answer_last_saved', None)
    #             }
    #         )

    #         return Response(
    #             ProgrammingQuestionProgressSerializer(progress).data,
    #             status=200)
    #     except ValueError as e:
    #         return Response({"error": "%s: %s" % (sys.exc_info()[0], e)},
    #                         status=400)

    #     return Response({"error": "oops..."}, status=400)

    @list_route(methods=['post'])
    def run(self, request):
        """
        Parameters: question(id), code
        """

        data = request.data
        student = request.user
        question_id = data.get('question', None)

        if not student or not question_id:
            return Response(
                {"message": "student or question empty"}, status=404)

        question = ProgrammingQuestion.objects.get(id=question_id)
        progress = ProgrammingQuestionProgress.objects.create(
            student=student,
            question=question,
            answer_last_saved=data.get('answer_last_saved', None)
        )

        unittests = UnitTest.objects.filter(
            question=question)

        if not unittests:
            return Respons({"error": "no unittest found"}, status=400)

        output = []
        for unittest in unittests:
            result = {}
            data = unittest.run(progress.answer_last_saved)
            result['is_correct'] = data.get('pass', False)
            result['visibility'] = unittest.visibility
            print data.get('visibility', 'nth')
            result['inputs'] = ", ".join(
                unittest.inputs) if result['visibility'] else "-"
            result['actual_output'] = data.get(
                'output', data.get('error', None)) if result['visibility'] else "-"
            result['expected_output'] = unittest.expected_output if result[
                'visibility'] else "-"

            output += [result]
        return Response(output)
