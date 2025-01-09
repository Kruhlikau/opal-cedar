from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from todo_app.auth_utils import make_auth_request, sync_and_flash
from todo_app.exceptions import PermissionDeniedException
from todo_app.utils import get_time_of_day, is_working_day

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    @sync_and_flash
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
                make_auth_request(
                    principal=principal,
                    method="GET",
                    original_url=self.request.build_absolute_uri(),
                    resource=f"task_{task.id}",
                    context={"time_of_day": get_time_of_day(), "is_working_day": is_working_day()},
                )
                allowed_tasks.append(task)
            except PermissionDeniedException:
                pass

        return Task.objects.filter(id__in=[task.id for task in allowed_tasks])

    @sync_and_flash
    def create(self, request, *args, **kwargs):
        """
        Handles task creation, ensuring authorization before proceeding.
        """
        user = request.user
        method = request.method
        original_url = request.build_absolute_uri()

        # Use Role as principal for create
        principal = f'Role::"{user.role}"'
        make_auth_request(
            principal=principal,
            method=method,
            original_url=original_url,
            resource=None,
            context={"time_of_day": get_time_of_day(), "is_working_day": is_working_day()},
        )

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
