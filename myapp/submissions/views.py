from rest_framework import viewsets, authentication, permissions, filters, status
from rest_framework.response import Response
from .serializers import (
    CodeSubmissionSerializer,
    BlanksSubmissionSerializer,
    McqSubmissionSerializer,
)
from .models import (
    CodeSubmission,
    BlanksSubmission,
    McqSubmission
)
from authnz.models import ProqodUser
from myapp.courses.models import Question
from myapp.analytics.models import PerformanceReport
# Create your views here.


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
                code=data.get('code', None)
                question=Question.objects.get(id=data.get('question',None))

            except:
                return Response({"message": "Required user, code and question params"}, status=400)

            # To be edited 
            complexity = -1
            memory = -1
            time = -1
            correctness = -1

            
            report = PerformanceReport(
                complexity=complexity,
                memory=memory,
                time=time,
                correctness=correctness
            )
            try:
                report.save()
            except:
                return Response({"message": "Failed to create report"}, status=400)
    
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


            return Response({"result": "submission complete"}, status=200)

        return Response({"message": "error"}, status=400)


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
