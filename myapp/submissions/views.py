from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .serializers import *
from .models import *
from myapp.courses.models import UnitTest
from myapp.analytics.models import PerformanceReport
from radon.metrics import mi_parameters, mi_compute
from radon import raw
# import sys


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

    def _test_with_fixed_unittest(self, unittests, code):
        """
        helper method:
        test with static inputs and expected output
        """

        ut_entries = []
        ut_passed = 0
        total_time = 0.
        memory = 0.
        for unittest in unittests:
            test = unittest.run(code)

            data = {
                'visibility': unittest.visibility,
                'inputs': ", ".join(unittest.inputs) if unittest.visibility else "-",
                'expected_output': unittest.expected_output if unittest.visibility else "-",
                'actual_output': test.get('output', test.get('error', None)) if unittest.visibility else "-",
                'is_correct': test.get('pass', False),
            }

            if data['inputs'] == "[u'[]']":
                data['inputs'] = ""

            if data['is_correct']:
                ut_passed += 1
                total_time += test['time']
                memory = max(memory, test['memory'])

            ut_entry = UnittestEntrySerializer(data=data)
            if ut_entry.is_valid():
                ut_entry.save()
                ute = UnittestEntry.objects.get(id=ut_entry.data['id'])
                ut_entries += [ute]
            else:
                return Response(ut_entry.errors, 400)
        time = (total_time / ut_passed) if ut_passed > 0 else '-1'

        return ut_entries, ut_passed, time, memory

    def _test_with_dynamic_unittest(self, tests, code):
        """
        helper method:
        test with dynamic unit test
        """

        test_entries = []
        test_passed = 0
        total_time = 0.
        memory = 0.
        for test in tests:
            test_result = test.dynamic_run(code)

            data = {
                'visibility': test.visibility,
                'expected_output': test_result.get('expected_output', None) if test.visibility else "-",
                'actual_output': test_result.get('output', test_result.get('error', None)) if test.visibility else "-",
                'is_correct': test_result.get('pass', False),
            }

            if data['is_correct']:
                test_passed += 1
                total_time += test_result['time']
                memory = max(memory, test_result['memory'])

            test_entry = UnittestEntrySerializer(data=data)
            if test_entry.is_valid():
                test_entry.save()
                ute = UnittestEntry.objects.get(
                    id=test_entry.data['id'])
                test_entries += [ute]
            else:
                return Response(test_entry.errors, 400)
        time = (total_time / test_passed) if test_passed > 0 else '-1'

        return test_entries, test_passed, time, memory

    def _eval_code_quality_metrics(self, code):
        complexity, loc, sloc, comments, multi, blank = [
            '-' for _ in xrange(6)]

        try:
            raw_analysis = raw.analyze(code)
            loc = raw_analysis.loc
            sloc = raw_analysis.sloc
            comments = raw_analysis.comments
            multi = raw_analysis.multi
            blank = raw_analysis.blank
        except:
            # log error
            pass

        complexity_eval = mi_parameters(code)

        if type(complexity_eval) == tuple:
            hv, complexity, lloc, _ = complexity_eval
            mi = mi_compute(hv, complexity, sloc, comments)

        return {'complexity': complexity,
                'loc': loc,
                'sloc': sloc,
                'comments': comments,
                'multi': multi,
                'blank': blank,
                'mi': mi,
                'hv': hv,
                'lloc': lloc,
                }

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

        # if dynamic, call dynamic unit test
        # tests = UnitTest.objects.filter(question=question)
        tests = 0
        if not tests:
            tests = DynamicTest.objects.filter(question=question)
            ut_entries, ut_passed, time, memory = self._test_with_dynamic_unittest(
                tests, code)
        else:
            ut_entries, ut_passed, time, memory = self._test_with_fixed_unittest(
                tests, code)

        assert len(ut_entries) > 0, "no unittests found"

        correctness = round((ut_passed + 0.0) / len(ut_entries), 2)
        size = len(code)

        # ==================== Quality Metrics ====================

        quality_metrics = self._eval_code_quality_metrics(code)

        report = PerformanceReport(
            memory=memory,
            time=time,
            correctness=correctness,
            size=size,
            complexity=quality_metrics['complexity'],
            halstead_volume=quality_metrics['hv'],
            lloc=quality_metrics['lloc'],
            loc=quality_metrics['loc'],
            sloc=quality_metrics['sloc'],
            comment_lines=quality_metrics['comments'],
            blank_lines=quality_metrics['blank'],
            multi_lines=quality_metrics['multi'],
            maintainability_index=quality_metrics['mi'],
        )

        try:
            report.save()

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

        subm = CodeSubmissionCreateSerializer(data=data)

        if subm.is_valid():
            subm.save()

            cs = CodeSubmission.objects.get(id=subm.data["id"])
            data = CodeSubmissionSerializer(cs).data

            return Response(data, status=201)
        else:
            return Response(subm.errors, status=400)

    @detail_route(methods=['get'],)
    def grade(self, request, pk=None):
        subm = CodeSubmission.objects.get(id=pk)
        assert subm is not None, "Cannot find submission"

        return Response(subm.get_grade(), status=200)


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
        solutions = BlankSolution.objects.filter(question=question)
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

    @detail_route(methods=['get'],)
    def grade(self, request, pk=None):
        subm = BlankSubmission.objects.get(id=pk)
        assert subm is not None, "Cannot find submission"

        return Response(subm.get_grade(), status=200)


class McqSubmissionViewSet(DefaultsMixin, viewsets.ModelViewSet):

    """ API endpoint for listing and creating Code Submission """
    queryset = McqSubmission.objects.order_by('date_created')
    serializer_class = McqSubmissionSerializer
    filter_fields = ['question', 'created_by']

    @detail_route(methods=['get'],)
    def grade(self, request, pk=None):
        subm = McqSubmission.objects.get(id=pk)
        assert subm is not None, "Cannot find submission"

        return Response(subm.get_grade(), status=200)


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

    @list_route(methods=['post', 'get', 'put'])
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
            result['inputs'] = ", ".join(
                unittest.inputs) if result['visibility'] else "-"
            result['actual_output'] = data.get(
                'output', data.get('error', None)) if result['visibility'] else "-"
            result['expected_output'] = unittest.expected_output if result[
                'visibility'] else "-"

            output += [result]
        return Response(output)
