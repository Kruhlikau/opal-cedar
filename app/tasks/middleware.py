import json
import requests
from django.http import JsonResponse


class TaskPolicyEnforcementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract necessary information from the request
        user = request.headers.get("user")
        method = request.method
        original_url = request.path

        # Prepare the authorization payload
        payload = {
            "principal": f'User::"{user}"',
            "action": f'Action::"{method.lower()}"',
            "resource": f"ResourceType::\"{original_url.split('/')[1]}\"",
            "context": self.get_request_body(request),
        }

        # Call the authorization service
        try:
            response = requests.post(
                "http://host.docker.internal:8180/v1/is_authorized",
                json=payload,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
            )
            response_data = response.json()
            import wdb
            wdb.set_trace()
            decision = response_data.get("decision")
        except Exception as e:
            return JsonResponse(
                {"error": "Authorization service error", "details": str(e)}, status=500
            )

        # If the decision is not "Allow", return a 403 response
        if decision != "Allow":
            return JsonResponse({"error": "Access Denied"}, status=403)

        # If authorized, proceed to the next middleware or view
        response = self.get_response(request)
        return response

    def get_request_body(self, request):
        """Safely parse the request body to extract JSON context."""
        try:
            if request.body:
                return json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            pass
        return {}
