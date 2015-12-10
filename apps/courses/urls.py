from django.conf.urls import *
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet)

# urlpatterns = [
# 	# url(
# 	# 		regex=r"^",
# 	# 		view=views.CourseCreateReadView.as_view(),
# 	# 		name="course_rest_api"
# 	# 	),

# 	# url(
# 	# 		regex=r"^(?P<id>[-\w]+)/$",
# 	# 		view=views.CourseReadUpdateDeleteView.as_view(),
# 	# 		name="course_rest_api"
# 	# 	),
# 	url(

# 			regex=r"^viewset/$",
# 			view=include(router.urls),
# 		),
# ]