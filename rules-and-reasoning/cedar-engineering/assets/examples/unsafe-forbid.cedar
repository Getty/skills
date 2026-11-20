// Deliberately unguarded optional context access: error does not imply Deny.
@id("permit-read")
permit (
  principal is Workshop::User,
  action == Workshop::Action::"read",
  resource is Workshop::Document
);
@id("forbid-with-missing-context")
forbid (
  principal is Workshop::User,
  action == Workshop::Action::"read",
  resource is Workshop::Document
)
when { context.blocked };
