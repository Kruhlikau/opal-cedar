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

    def make_auth_request(self, principal, method, original_url, resource, context=None):
        """
        Make the authorization request to Cedar with a specified principal.
        """
        response = requests.post(
            "http://host.docker.internal:8180/v1/is_authorized",
            json={
                "principal": principal,
                "action": f'Action::"{method.lower()}"',
                "resource": f'ResourceType::"{resource}"',
                "context": context or {},
            },
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        response.raise_for_status()
        result = response.json()
        if result.get("decision") != "Allow":
            raise PermissionDeniedException(detail="Access denied.")
        return result

    @sync_entities_with_cedar
    def get_queryset(self):
        """
        Restrict tasks to those allowed by Cedar for the authenticated user.
        """
        user = self.request.user
        queryset = Task.objects.all()
        allowed_tasks = []

        for task in queryset:
            try:
                principal = f'User::"{user.username}"'
                self.make_auth_request(
                    principal=principal,
                    method="GET",
                    original_url=self.request.build_absolute_uri(),
                    resource=f"task_{task.id}",
                )
                allowed_tasks.append(task)
            except PermissionDeniedException:
                pass

        return Task.objects.filter(id__in=[task.id for task in allowed_tasks])

    @sync_entities_with_cedar
    def create(self, request, *args, **kwargs):
        """
        Handles task creation, ensuring authorization before proceeding.
        """
        user = request.user
        method = request.method
        original_url = request.build_absolute_uri()

        # Use Role as principal for create
        principal = f'Role::"{user.role}"'
        self.make_auth_request(principal, method, original_url, "NewTask", request.data)

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
