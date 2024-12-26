import requests
from rest_framework.exceptions import APIException
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer
from .utils import sync_entities_with_cedar


class PermissionDeniedException(APIException):
    status_code = 403
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def make_auth_request(self, user, method, original_url, context=None):
        """
        Make the authorization request to Cedar.
        """
        response = requests.post(
            "http://host.docker.internal:8180/v1/is_authorized",
            json={
                "principal": f'Role::"{user.role}"',
                "action": f'Action::"{method.lower()}"',
                "resource": 'ResourceType::"NewTask"',
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        response.raise_for_status()
        result = response.json()
        if result.get("decision") != "Allow":
            raise PermissionDeniedException(detail="Access denied.")
        return result

    @sync_entities_with_cedar
    def create(self, request, *args, **kwargs):
        """
        Handles task creation, ensuring authorization before proceeding.
        """
        user = request.user
        method = request.method
        original_url = request.build_absolute_uri()

        self.make_auth_request(user, method, original_url, request.data)

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """
        Saves the new task, associating it with the authenticated user.
        """
        serializer.save(owner=self.request.user)


class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
