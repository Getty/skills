package workspace.authz_test

import rego.v1
import data.workspace.authz

test_owner_read if {
    authz.allow == true with input as {"subject": "alice", "action": "read", "resource": {"tenant": "t1", "owner": "alice"}}
}

test_editor_write if {
    authz.allow == true with input as {"subject": "bob", "action": "write", "resource": {"tenant": "t1", "owner": "alice"}}
}

test_cross_tenant_denied if {
    authz.allow == false with input as {"subject": "bob", "action": "write", "resource": {"tenant": "t2", "owner": "bob"}}
}

test_inactive_denied if {
    authz.allow == false with input as {"subject": "carol", "action": "read", "resource": {"tenant": "t1", "owner": "carol"}}
}

test_unknown_subject_denied if {
    authz.allow == false with input as {"subject": "nobody", "action": "read", "resource": {"tenant": "t1", "owner": "nobody"}}
}

test_missing_fields_denied if { authz.allow == false with input as {} }
test_wrong_subject_type_denied if {
    authz.allow == false with input as {"subject": 7, "action": "read", "resource": {"tenant": "t1", "owner": "alice"}}
}

test_owner_write_denied if {
    authz.allow == false with input as {"subject": "alice", "action": "write", "resource": {"tenant": "t1", "owner": "alice"}}
}

test_unknown_action_denied if {
    authz.allow == false with input as {"subject": "bob", "action": "delete", "resource": {"tenant": "t1", "owner": "alice"}}
}

test_null_input_denied if { authz.allow == false with input as null }
