from rest_framework import (viewsets,
                            authentication,
                            permissions,
                            filters,
                            mixins
                            )
# from rest_framework.response import Response
from .models import ProqodUser

from .serializers import UserSerializer
import rest_framework_jwt

class DefaultsMixin(object):

    """
    Default settings for view auth, permissions,
    filtering and pagination
    """

    authentication_classes = (
        rest_framework_jwt.authentication.JSONWebTokenAuthentication,
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
                                    viewsets.ReadOnlyModelViewSet):

    """ API endpoint for users """
    queryset = ProqodUser.objects.all()
    serializer_class = UserSerializer
    filter_fields = ['user_type', 'is_admin', 'id', 'sid']

    # def get_permissions(self):
    #     if self.action in ('create', 'update', 'destroy', 'partial_update'):
    #         self.permission_classes = [permissions.IsAdminUser, ]
    #     return super(self.__class__, self).get_permissions()
