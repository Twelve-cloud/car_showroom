from rest_framework.permissions import IsAuthenticated, IsAdminUser
from auth.serializers import BasicUserSerializer, FullUserSerializer
from auth.permissions import IsUserOwner
from rest_framework import viewsets
from auth.models import User


class UserViewSet(viewsets.ModelViewset):
    queryset = User.objects.all()
    permission_map = {
        'create': (
            ~ IsAuthenticated | IsAdminUser,
        ),
        'list': (
            IsAuthenticated,
        ),
        'retrieve': (
            IsAuthenticated,
        ),
        'update': (
            IsAuthenticated & IsUserOwner,
        ),
        'partial_update': (
            IsAuthenticated & IsUserOwner,
        ),
        'destroy': (
            IsAuthenticated & (IsUserOwner | IsAdminUser),
        ),
    }

    def get_permissions(self):
        self.permission_classes = self.permission_map.get(self.action, [])
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            if self.action == 'retrieve':
                self.user = self.get_object()
                if self.request.user == self.user:
                    return FullUserSerializer
            return BasicUserSerializer
        else:
            return FullUserSerializer

    def create(self, requests, *args, **kwargs):
        pass

    def update(self, requests, *args, **kwargs):
        pass

    def destroy(self, requests, *args, **kwargs):
        pass

