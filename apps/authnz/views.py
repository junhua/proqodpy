# from django.shortcuts import render

# # https://docs.djangoproject.com/en/1.9/ref/contrib/auth/
# from django.contrib.auth import get_user_model, user_logged_in, user_logged_out
# from django.contrib.auth.tokens import default_token_generator

# from rest_framework import permissions, generics, status
# from rest_framework.authtoken.models import Token
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from djoser import signals, settings, utils, views, serializers

# from .serializers import StudentRegistrationSerializer
# from .models import Teacher, Student, TeachingAssistant


# User = get_user_model()

# class CustomRegistrationView(utils.SendEmailViewMixin, generics.CreateAPIView):

#     """
#     Use this endpoint to register new user.
#     """
#     serializer_class = StudentRegistrationSerializer
#     permission_classes = (
#         permissions.AllowAny,
#     )
#     token_generator = default_token_generator
#     subject_template_name = 'activation_email_subject.txt'
#     plain_body_template_name = 'activation_email_body.txt'

#     def perform_create(self, serializer):
#         print serializer
#         instance = serializer.save()
#         signals.user_registered.send(
#             sender=self.__class__, user=instance, request=self.request)
#         print settings.get('SEND_ACTIVATION_EMAIL')
#         if settings.get('SEND_ACTIVATION_EMAIL'):
#             self.send_email(**self.get_send_email_kwargs(instance))

#     def get_email_context(self, user):
#         context = super(CustomRegistrationView, self).get_email_context(user)
#         context['url'] = settings.get('ACTIVATION_URL').format(**context)
#         return context


# @api_view(['GET'])
# def get_user_info(request):
#     """
#     Method to overwrite djoser auth/me to return the extra attribute user type
#     """
#     if request.user.is_anonymous():
#         #logger.debug("User not found, request.user is empty")
#         return Response(status=401)

#     teachers = Teacher.objects.filter(user=request.user)
#     students = Student.objects.filter(user=request.user)
#     if len(teachers) > 0:
#         user_type = "teacher"
#         if len(students) > 0:
#             # This case should not happen
#             user_type = "teacher_and_student"
#     elif len(students) > 0:
#         user_type = "student"
#     else:
#         user_type = "undefined"
#     user_data = serializers.UserSerializer(request.user).data
#     user_data.update({'type': user_type})
#     return Response(data=user_data)


# class TeacherLoginView(views.LoginView):

#     """
#     Custom login view for teachers, reusing djoser serializer to validate
#     credentials
#     """

#     serializer_class = serializers.LoginSerializer
#     permission_classes = (
#         permissions.AllowAny,
#     )

#     def action(self, serializer):
#         user = serializer.user
#         teachers = Teacher.objects.filter(user=user)
#         if len(teachers) > 0:
#             token, _ = Token.objects.get_or_create(user=user)
#             user_logged_in.send(sender=user.__class__, request=self.request, user=user)
#             return Response(
#                 data=serializers.TokenSerializer(token).data,
#                 status=status.HTTP_200_OK)
#         else:
#             Token.objects.filter(user=user).delete()
#             user_logged_out.send(sender=user.__class__, request=self.request, user=user)
#         return Response(
#             data={'error': "Teacher credentials not found"},
#             status=401,
#         )
