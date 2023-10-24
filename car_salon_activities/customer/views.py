from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from customer.models import CustomerModel, CustomerHistory
from customer.serializers import CustomerSerializer, CustomerHistorySerializer


class CustomerViewSet(viewsets.ModelViewSet):
    permission_map = {
        'create': [
            # IsAuthenticated & ~IsUserHasCustomer,
        ],
        'list': [
            IsAuthenticated,
        ],
        'retrieve': [
            IsAuthenticated,
        ],
        'update': [
            IsAdminUser,
        ],
        'partial_update': [
            IsAdminUser,
        ],
        'destroy': [
            # IsAuthenticated & (IsAdminUser | IsCustomerOwner),
        ],
    }

    def get_queryset(self):
        if self.action == 'get_statistics':
            return CustomerHistory.objects.filter(is_active=True)
        return CustomerModel.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'get_statistics':
            return CustomerHistorySerializer
        return CustomerSerializer

    def get_permissions(self) -> list:
        self.permission_classes = self.permission_map.get(self.action, [])
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.is_active = False
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def get_statistics(self, request):
        history = self.get_queryset()
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
