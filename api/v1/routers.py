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

router.register(r'courses', CourseViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'mcq', McqQuestionViewSet)
router.register(r'blank_qn', BlankQuestionViewSet)
router.register(r'prog_qn', ProgrammingQuestionViewSet)
router.register(r'multiple_choice', MultipleChoiceViewSet)
router.register(r'blank_qn_content', BlankQuestionContentViewSet)


