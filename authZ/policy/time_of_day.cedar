// CBAC
forbid(
  principal,
  action,
  resource
)
when {
  context.time_of_day != "morning"
};