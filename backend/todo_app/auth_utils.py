from functools import wraps

from accounts.models import CustomUser
import requests
from rest_framework.exceptions import APIException
from tasks.models import Task
from todo_app.exceptions import PermissionDeniedException


HTTP_METHODS = ["POST", "PUT", "GET", "DELETE"]


def flash_data():
    """
    Decorator to send an empty payload to clear data on the Cedar data store.
    """
    response = requests.put(
        "http://host.docker.internal:8180/v1/data",
        json=[],
        headers={"Content-Type": "application/json"},
    )
    if response.status_code != 200:
        raise APIException(f"Failed to flash data.")


def sync_entities_with_cedar(func):
    """
    Decorator to dynamically build and sync entities with the Cedar data store.
    """

    def build_entities():
        """
        Dynamically build entities JSON from CustomUser and Task models.
        """
        # User entities
        user_entities = [
            {
                "uid": {"id": f"{user.username}", "type": "User"},
                "attrs": {"id": user.id, "username": user.username},
                "parents": [{"id": user.role, "type": "Role"}],
            }
            for user in CustomUser.objects.all()
        ]

        # Role entities
        role_entities = [
            {"uid": {"id": role[0], "type": "Role"}, "attrs": {}, "parents": []}
            for role in CustomUser._meta.get_field("role").choices
        ]

        # Task entities (as resources)
        task_entities = [
            {
                "uid": {"id": f"task_{task.id}", "type": "Task"},
                "attrs": {"owner": task.owner.username, "access_level": task.access_level},
                "parents": [],
            }
            for task in Task.objects.all()
        ]

        # Action entities
        action_entities = [
            {"uid": {"id": action, "type": "Action"}, "attrs": {}, "parents": []}
            for action in HTTP_METHODS
        ]

        # Combine all entities
        return user_entities + role_entities + task_entities + action_entities

    def sync_with_cedar():
        """
        Sync the dynamically built entities with the Cedar data store.
        """
        entities = build_entities()
        response = requests.put(
            "http://host.docker.internal:8180/v1/data",
            json=entities,
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 200:
            raise APIException(detail="Failed to sync entities with Cedar.")

    @wraps(func)
    def wrapper(*args, **kwargs):
        sync_with_cedar()  # Ensure entities are synced before the function execution
        return func(*args, **kwargs)

    return wrapper


def sync_and_flash(func):
    """
    Composite decorator that syncs entities with Cedar and flashes data.
    """

    @sync_entities_with_cedar
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        flash_data()
        return result

    return wrapper


def make_auth_request(principal, method, original_url, resource, context=None):
    """
    Make the authorization request to Cedar with a specified principal.
    """
    response = requests.post(
        "http://host.docker.internal:8180/v1/is_authorized",
        json={
            "principal": principal,
            "action": f'Action::"{method}"',
            "resource": f'Task::"{resource}"' if resource else None,
            "context": context or {},
        },
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    response.raise_for_status()
    result = response.json()
    if result.get("decision") != "Allow":
        raise PermissionDeniedException(detail="Access denied.")
    return result
