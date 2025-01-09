// CBAC
forbid(
  principal,
  action,
  resource
)
when {
  context.time_of_day != "morning"  &&
  context.is_working_day == true
};