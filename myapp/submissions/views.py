from rest_framework import viewsets, authentication, permissions, filters, status
from rest_framework.decorators import detail_route, list_route

from rest_framework.response import Response
from .serializers import *
from .models import *
from authnz.models import ProqodUser
from myapp.courses.models import Question
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
    filter_fields = ['question']

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
                question = data.get('question', None)
            except:
                return Response({"message": "Required user, code and question params"}, status=400)

            # To be edited
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
                    {"message": "Failed to create report"},
                    status=400
                )

            subm = CodeSubmission(
                created_by=user,
                code=code,
                question=question,
                performance_report=report
            )

            try:
                subm.save()
            except:
                return Response(
                    {"message": "Failed to create submission"},
                    status=400
                )
            data = CodeSubmissionSerializer(subm).data
            # return Response({"message": "submission completed"}, status=200)
            return Response(data, status=200)

        return Response({"message": "error"}, status=400)

    @list_route(methods=['post'])
    def run(self, request):
        data = request.data
        code = data.get('code', None)


class BlanksSubmissionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Code Submission """
    queryset = BlanksSubmission.objects.order_by('date_created')
    serializer_class = BlanksSubmissionSerializer
    filter_fields = ['question']


class McqSubmissionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Code Submission """
    queryset = McqSubmission.objects.order_by('date_created')
    serializer_class = McqSubmissionSerializer
    filter_fields = ['question']


class McqProgressViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Mcq Progress """
    queryset = McqProgress.objects.all()
    serializer_class = McqProgressSerializer
    filter_fields = ['question', 'student']


class BlankQuestionProgressViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Blank question progress """
    queryset = BlankQuestionProgress.objects.all()
    serializer_class = BlankQuestionProgressSerializer
    filter_fields = ['question', 'student']


class ProgrammingQuestionProgressViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Programming Question Progress """
    queryset = ProgrammingQuestionProgress.objects.all()
    serializer_class = ProgrammingQuestionProgressSerializer
    filter_fields = ['question', 'student']

    def create(self, request):
        data = request.data
        student = request.user
        question = data.get('question', None)

        if not student or not question:
            return Response({"message": "student or question empty"}, status=404)

        try:
            progress, _ = ProgrammingQuestionProgress.objects.update_or_create(
                student=student,
                question=question,
                defaults={
                    'answer_last_saved': data.get('answer_last_saved', None)
                }
            )
            return Response(ProgrammingQuestionProgressSerializer(progress).data, status=200)
        except:
            return Response({"error": sys.exc_info()[0]}, status=400)
        return Response({"error": "oops..."}, status=400)
