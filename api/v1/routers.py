from rest_framework.routers import DefaultRouter

from myapp.courses.views import (
    CourseViewSet,
    AssessmentViewSet,
    McqQuestionViewSet,
    BlankQuestionViewSet,
    ProgrammingQuestionViewSet,
    MultipleChoiceViewSet,
    BlankQuestionContentViewSet,
    QuestionViewSet,
    TestCaseViewSet,
)

from myapp.analytics.views import (
    PerformanceReportViewset,
    PeerRankReportViewset,
    PeerRankViewset,
)

from myapp.submissions.views import (
    CodeSubmissionViewSet,
    BlanksSubmissionViewSet,
    McqSubmissionViewSet,
)

router = DefaultRouter()

# Courses
router.register(r'courses', CourseViewSet, base_name='courses')
router.register(r'assessments', AssessmentViewSet, base_name='assessments')
router.register(r'mcq', McqQuestionViewSet, base_name='mcq')
router.register(
    r'blank_qns', BlankQuestionViewSet, base_name='blank questions')
router.register(
    r'prog_qns', ProgrammingQuestionViewSet, base_name='programming questions')
router.register(
    r'questions', QuestionViewSet, base_name='questions')

router.register(
    r'mcq_choices', MultipleChoiceViewSet, base_name='multiple_choices')

router.register(r'blank_qn_content', BlankQuestionContentViewSet,
                base_name='blank question content')

# Analytics
router.register(r'performance_reports', PerformanceReportViewset,
                base_name='perormance report')
router.register(r'peer_rank_reports', PeerRankReportViewset,
                base_name='Peer Rank Report Viewset')
router.register(r'peer_rank', PeerRankViewset,
                base_name='peer rank')

# Submissions
router.register(r'code_submissions', CodeSubmissionViewSet,
                base_name='code submissions')
router.register(r'blanks_submissions', BlanksSubmissionViewSet,
                base_name='blanks submissions')
router.register(r'mcq_submissions', McqSubmissionViewSet,
                base_name='mcq submissions')
router.register(r'testcases', TestCaseViewSet,
                base_name='test cases')