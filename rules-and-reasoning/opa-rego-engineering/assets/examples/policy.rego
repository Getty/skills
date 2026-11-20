package workspace.authz

import rego.v1

default allow := false

valid_request if {
    is_object(input)
    is_string(input.subject)
    input.subject != ""
    is_string(input.action)
    is_object(input.resource)
    is_string(input.resource.tenant)
    input.resource.tenant != ""
    is_string(input.resource.owner)
    input.resource.owner != ""
}

eligible(principal) if {
    principal.active == true
    is_string(principal.tenant)
    is_array(principal.roles)
    every role in principal.roles { is_string(role) }
}

allow if {
    valid_request
    input.action == "read"
    principal := data.identity.subjects[input.subject]
    eligible(principal)
    principal.tenant == input.resource.tenant
    input.resource.owner == input.subject
}

allow if {
    valid_request
    input.action in {"read", "write"}
    principal := data.identity.subjects[input.subject]
    eligible(principal)
    principal.tenant == input.resource.tenant
    "editor" in principal.roles
}

decision := {"allow": allow, "policy_revision": "workspace-example-v1"}
