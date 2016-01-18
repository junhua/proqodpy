from rest_framework.routers import DefaultRouter

from myapp.courses.views import *

from myapp.analytics.views import *

from myapp.submissions.views import *

router = DefaultRouter()

# Courses
router.register(r'courses', CourseViewSet, base_name='courses')
router.register(r'assessments', AssessmentViewSet, base_name='assessments')

router.register(r'blank_qns',
                BlankQuestionViewSet, base_name='blank questions')
router.register(r'blank_qn_content', BlankQuestionContentViewSet,
                base_name='blank question content')
router.register(r'blanks_submissions', BlankSubmissionViewSet,
                base_name='blanks submissions')
router.register(r'blank_solution', BlankSolutionViewSet,
                base_name='blank solution')
router.register(r'blank_qn_progress', BlankQuestionProgressViewSet,
                base_name='blank qustion progress')
router.register(r'checkoff_qns', CheckoffQuestionViewSet,
                base_name='checkoff questions')
router.register(r'checkoff_submissions', CheckoffSubmissionViewSet,
                base_name='checkoff submissions')
router.register(r'mcq', McqViewSet,
                base_name='mcq')
router.register(r'mcq_choices', MultipleChoiceViewSet,
                base_name='multiple_choices')
router.register(r'mcq_submissions', McqSubmissionViewSet,
                base_name='mcq submissions')
router.register(r'mcq_progress', McqProgressViewSet,
                base_name='MCQ progress')
router.register(r'prog_qns', ProgrammingQuestionViewSet,
                base_name='programming questions')
router.register(r'code_submissions', CodeSubmissionViewSet,
                base_name='code submissions')
router.register(r'performance_reports', PerformanceReportViewset,
                base_name='perormance report')
router.register(r'unittests', UnitTestViewSet,
                base_name='unit tests')
router.register(r'prog_qn_progress', ProgrammingQuestionProgressViewSet,
                base_name='programming question progress')

router.register(r'acad_report', AcademicReportViewset,
                base_name='academic report')

# router.register(r'unittest_entry', UnittestEntryViewSet,
#                 base_name='unittest entry')

# Analytics

# router.register(r'peer_rank_reports', PeerRankReportViewset,
#                 base_name='Peer Rank Report Viewset')
# router.register(r'peer_rank', PeerRankViewset,
#                 base_name='peer rank')

# Submissions
