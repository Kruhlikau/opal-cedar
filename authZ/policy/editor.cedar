// RBAC
permit(
    principal in Role::"editor",
    action in [Action::"POST", Action::"PUT", Action::"GET"],
    resource
);
