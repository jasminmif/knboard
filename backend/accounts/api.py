from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import filters
from accounts.models import Avatar
from boards.models import Board

from accounts.serializers import AvatarSerializer, UserSerializer, UserDetailSerializer

User = get_user_model()


class ExcludeBoardMembersFilter(filters.BaseFilterBackend):
    """
    Filter that only shows members that are not a member of board.
    """
    filter_param = "excludemembers"

    def filter_queryset(self, request, queryset, view):
        board_id = request.query_params.get(self.filter_param)
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            return queryset

        return queryset.exclude(id__in=board.members.all())


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, ExcludeBoardMembersFilter]
    search_fields = ["username"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        return super().get_serializer_class()


class AvatarViewSet(ReadOnlyModelViewSet):
    serializer_class = AvatarSerializer
    queryset = Avatar.objects.all()
    permission_classes = [IsAuthenticated]
