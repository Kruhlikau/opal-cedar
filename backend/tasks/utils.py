import requests
from functools import wraps
from rest_framework.exceptions import APIException

from .models import Task
from accounts.models import CustomUser


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
                "attrs": {},
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
            {"uid": {"id": f"task_{task.id}", "type": "ResourceType"}, "attrs": {}, "parents": []}
            for task in Task.objects.all()
        ]

        # Action entities
        action_entities = [
            {"uid": {"id": action, "type": "Action"}, "attrs": {}, "parents": []}
            for action in ["post", "put", "get", "delete"]
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
