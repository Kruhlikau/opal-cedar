// ABAC
permit(
  principal,
  action,
  resource
)
when {
  resource has owner &&
  resource.owner == principal.username
};