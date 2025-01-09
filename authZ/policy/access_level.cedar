// ABAC
forbid(
  principal,
  action,
  resource
)
when {
  resource has access_level &&
  resource.access_level != "public"
};