from rest_framework.routers import DefaultRouter

from myapp.courses.views import (
    CourseViewSet,
    AssessmentViewSet,
    McqQuestionViewSet,
    BlankQuestionViewSet,
    ProgrammingQuestionViewSet,
    MultipleChoiceViewSet,
    BlankQuestionContentViewSet,

)

router = DefaultRouter()

router.register(r'courses', CourseViewSet, base_name='courses')
router.register(r'assessments', AssessmentViewSet, base_name='assessments')
router.register(r'mcq', McqQuestionViewSet, base_name='mcq')
router.register(r'blank_qns', BlankQuestionViewSet, base_name='blank questions')
router.register(
    r'prog_qns', ProgrammingQuestionViewSet, base_name='programming questions')

router.register(
    r'mcq_choices', MultipleChoiceViewSet, base_name='multiple_choices')

router.register(r'blank_qn_content', BlankQuestionContentViewSet,
                base_name='blank question content')
