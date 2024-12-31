// Permit users to view tasks they own
permit (
  principal,
  action == Action::"get",
  resource
)
when {
  resource.owner == principal
};