from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer, HistoricalTaskSerializer, UserSerializer
from .filters import TaskFilter


# https://www.django-rest-framework.org/api-guide/viewsets/
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()  # objects to retrieve
    serializer_class = TaskSerializer  # we link TaskSerializer to the viewset

    filter_backends = [DjangoFilterBackend]  # Enables filtering
    filterset_class = TaskFilter  # Links the custom filter class

    # https://www.django-rest-framework.org/api-guide/views/
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        task = self.get_object()
        history = task.history.all()
        return Response(HistoricalTaskSerializer(history, many=True).data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)