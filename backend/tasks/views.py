from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from todo_app.auth_utils import make_auth_request, sync_and_flash
from todo_app.exceptions import PermissionDeniedException
from todo_app.utils import get_time_of_day, is_working_day

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer

    @sync_and_flash
    def get_queryset(self):
        """
        Restrict tasks to those allowed by Cedar for the authenticated user.
        """
        user = self.request.user
        queryset = Task.objects.all()

        task_ids = queryset.values_list("id", flat=True)
        allowed_ids = []

        for task_id in task_ids:
            try:
                principal = f'User::"{user.username}"'
                make_auth_request(
                    principal=principal,
                    method="GET",
                    original_url=self.request.build_absolute_uri(),
                    resource=f"task_{task_id}",
                    context={"time_of_day": get_time_of_day(), "is_working_day": is_working_day()},
                )
                allowed_ids.append(task_id)
            except PermissionDeniedException:
                continue

        return queryset.filter(id__in=allowed_ids).order_by("-id")

    @sync_and_flash
    def create(self, request, *args, **kwargs):
        """
        Handles task creation, ensuring authorization before proceeding.
        """
        user = request.user
        method = request.method
        original_url = request.build_absolute_uri()

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

    @sync_and_flash
    def get_object(self):
        """
        Retrieve a task after ensuring the user is authorized to access it.
        """
        user = self.request.user
        task = super().get_object()

        try:
            principal = f'User::"{user.username}"'
            make_auth_request(
                principal=principal,
                method="GET",
                original_url=self.request.build_absolute_uri(),
                resource=f"task_{task.id}",
                context={"time_of_day": get_time_of_day(), "is_working_day": is_working_day()},
            )
        except PermissionDeniedException:
            raise PermissionDeniedException("You do not have permission to access this task.")

        return task

    @sync_and_flash
    def update(self, request, *args, **kwargs):
        """
        Handles updating a task after ensuring authorization.
        """
        user = request.user
        task = self.get_object()

        principal = f'User::"{user.username}"'
        make_auth_request(
            principal=principal,
            method="PUT",
            original_url=request.build_absolute_uri(),
            resource=f"task_{task.id}",
            context={"time_of_day": get_time_of_day(), "is_working_day": is_working_day()},
        )

        return super().update(request, *args, **kwargs)

    @sync_and_flash
    def destroy(self, request, *args, **kwargs):
        """
        Handles deleting a task after ensuring authorization.
        """
        user = request.user
        task = self.get_object()

        principal = f'User::"{user.username}"'
        make_auth_request(
            principal=principal,
            method="DELETE",
            original_url=request.build_absolute_uri(),
            resource=f"task_{task.id}",
            context={"time_of_day": get_time_of_day(), "is_working_day": is_working_day()},
        )

        return super().destroy(request, *args, **kwargs)
