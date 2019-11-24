from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe.serializers import TagSerializer


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in DB"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_queryset(self):
        """return qs for current user"""
        return self.queryset.filter(user=self.request.user).order_by("-name")
