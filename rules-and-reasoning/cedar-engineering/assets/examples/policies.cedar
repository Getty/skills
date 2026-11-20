@id("read-team-document")
permit (
  principal is Workshop::User in Workshop::Team::"blue",
  action == Workshop::Action::"read",
  resource is Workshop::Document
)
when {
  principal.tenant == resource.tenant &&
  (!resource.confidential || context.mfa)
};

@id("write-own-document")
permit (
  principal is Workshop::User,
  action == Workshop::Action::"write",
  resource is Workshop::Document
)
when {
  principal.tenant == resource.tenant &&
  resource.owner == principal &&
  context.mfa
};

@id("deny-suspended-user")
forbid (
  principal is Workshop::User,
  action,
  resource
)
when { principal.suspended };
