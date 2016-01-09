from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.decorators import detail_route, list_route

from rest_framework.response import Response
from .serializers import *
from .models import *
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
        serializer = CodeSubmissionSerializer(data=data)

        if serializer.is_valid():
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

            # PERFORMANCE REPORT (To be edited)
            complexity = -1
            memory = -1
            time = PerformanceReport.objects.time_exec(code)
            correctness = -1
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
            except:
                return Response(
                    {"message": "Failed to create performance report"},
                    status=404
                )

            # SCORE

            # unittests = UnitTest.objects.filter(question=question)
            # for unittest in unittests:
            #     test_code = unittest.run(code)
            #     print test_code
            # unittest_results = []

            # print "***"
            # print type(unittests[0].expected_output)

            subm = CodeSubmission(
                created_by=user,
                code=code,
                question=question,
                performance_report=report,
                type=0
            )
            subm.save()
            try:
                subm.save()
            except:
                print sys.exc_info()[0]
                return Response(
                    {"message": "Failed to create submission"},
                    status=400
                )
            data = CodeSubmissionSerializer(subm).data
            # return Response({"message": "submission completed"}, status=200)
            return Response(data, status=200)

        return Response({"message": "error"}, status=400)

    # @list_route(methods=['post'])
    # def run(self, request):
    #     data = request.data
    #     code = data.get('code', None)


class BlanksSubmissionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Code Submission """
    queryset = BlanksSubmission.objects.order_by('date_created')
    serializer_class = BlanksSubmissionSerializer
    filter_fields = ['question', 'created_by']


class McqSubmissionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Code Submission """
    queryset = McqSubmission.objects.order_by('date_created')
    serializer_class = McqSubmissionSerializer
    filter_fields = ['question','created_by']


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

    def create(self,request):
        """
        Parameters: question(id), answer
        """
        data = request.data
        student = request.user
        question_id = data.get('question', None)

        if not student or not question_id:
            return Response({"message": "student or question empty"}, status=404)

        try:

            question = Mcq.objects.get(id=question_id)
            progress, _ = McqProgress.objects.update_or_create(
                student=student,
                question=question,
                defaults={
                    'choice': MultipleChoice.objects.get(id=data.get('choice', None))
                }
            )

            return Response(McqProgressSerializer(progress).data, status=200)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=400)
            # return Response({"error": str(sys.exc_info()[0])}, status=400)

        return Response({"error": "oops..."}, status=400)

class BlankQuestionProgressViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Blank question progress """
    queryset = BlankQuestionProgress.objects.all()
    serializer_class = BlankQuestionProgressSerializer
    filter_fields = ['question', 'student']

    def create(self,request):
        """
        Parameters: question(id), answer_last_saved
        """
        data = request.data
        student = request.user
        question_id = data.get('question', None)

        if not student or not question_id:
            return Response({"message": "student or question empty"}, status=404)

        try:

            question = BlankQuestion.objects.get(id=question_id)
            progress, _ = BlankQuestionProgress.objects.update_or_create(
                student=student,
                question=question,
                defaults={
                    'answer_last_saved': data.get('answer_last_saved', None)
                }
            )

            return Response(McqProgressSerializer(progress).data, status=200)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=400)
            # return Response({"error": str(sys.exc_info()[0])}, status=400)

        return Response({"error": "oops..."}, status=400)


class ProgrammingQuestionProgressViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Programming Question Progress """
    queryset = ProgrammingQuestionProgress.objects.all()
    serializer_class = ProgrammingQuestionProgressSerializer
    filter_fields = ['question', 'student']

    def create(self, request):
        """
        Parameters: question(id), code
        """
        data = request.data
        student = request.user
        question_id = data.get('question', None)

        if not student or not question_id:
            return Response({"message": "student or question empty"}, status=404)

        try:

            question = ProgrammingQuestion.objects.get(id=question_id)
            progress, _ = ProgrammingQuestionProgress.objects.update_or_create(
                student=student,
                question=question,
                defaults={
                    'answer_last_saved': data.get('answer_last_saved', None)
                }
            )

            return Response(ProgrammingQuestionProgressSerializer(progress).data, status=200)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=400)
            # return Response({"error": str(sys.exc_info()[0])}, status=400)

        return Response({"error": "oops..."}, status=400)
