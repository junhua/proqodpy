from rest_framework import (viewsets,
                            authentication,
                            permissions,
                            filters,
                            mixins
                            )
# from rest_framework.response import Response
from .models import ProqodUser

from djoser.serializers import UserSerializer


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
        # permissions.IsAuthenticated,
        permissions.IsAdminUser,
    )
    paginate_by = 25
    # paginate_by_param = "school"
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class ProqodUserListRetrieveViewSet(DefaultsMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):

    """ API endpoint for users """
    queryset = ProqodUser.objects.all()
    serializer_class = UserSerializer
    filter_fields = ['user_type', 'is_admin']

    # def get_permissions(self):
    #     if self.action in ('create', 'update', 'destroy', 'partial_update'):
    #         self.permission_classes = [permissions.IsAdminUser, ]
    #     return super(self.__class__, self).get_permissions()
