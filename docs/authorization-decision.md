# Authorization ownership decision

Status: accepted design direction, 2 November 2026.

## Decision

Centrally administer roles, permissions, entitlement mappings, scope grants and shared policies. Each resource-owning microservice validates tokens and evaluates both RBAC and ABAC. BFF owns browser sessions, CSRF and server-side token lifecycle. A private gateway is optional for routing or traffic controls and is not required for RBAC.

## Default request path

Browser -> ALB/public edge -> BFF -> private microservice -> authorized transaction.

Authorization management -> authenticated/versioned policy distribution -> service-local evaluator. The control-plane path is not a mandatory synchronous business-request hop.

## Consequences

This removes duplicated gateway business-permission mappings and a mandatory central decision dependency. It requires consistent permission vocabulary, governed policy distribution and contract tests across languages. Local RBAC/ABAC must cover every controller, application-service entry, list, export, bulk operation and background/workload path.

### Central administration with local enforcement

The Authorization Management Service owns versioned role definitions, issuer-scoped entitlement mappings, permissions, named policies and scope grants. It authenticates service workloads and publishes approved, signed/versioned policy bundles or authenticated snapshots. It is a control-plane component, not a required synchronous hop for every business request. Each service validates the configured publisher/signature and schema, enforces version/validity bounds, and evaluates both RBAC and ABAC locally. Spring services may use shared policy classes; polyglot services may use a local policy evaluator with the same versioned contract. Domain services own their resource-specific rules.

Policies use stable permission names, independent of service deployment names. A service selects the required permission from its controlled operation mapping. It supplies the verified issuer/subject, trusted entitlements and authoritative resource attributes; the browser cannot select its actor, policy, permission or scope grant. Query, bulk and export paths enforce the same rules.

Policy distribution uses change notifications plus periodic reconciliation and a bounded maximum age. A service may continue using a last-known-good snapshot only while it remains explicitly valid and permitted by policy. Missing, invalid or expired mandatory policy/entitlement data causes a controlled 503 with no business mutation; a valid policy denial is 403. Sensitive operations can require a fresh entitlement check through an authenticated central endpoint under a documented availability contract.

Log policy version, entitlement source/freshness and a safe decision reason. Revocation targets must cover token claim age, policy/grant caches and notification delay. Refreshing a policy bundle does not remove stale group claims from an existing JWT; meeting a tighter SLA requires token revocation, fresh entitlement resolution or reauthentication. Never silently extend validity during an outage.

## Acceptance checks

- Wrong issuer/audience/expired token is rejected at every service, even when callers bypass the edge from a test network.
- Valid identity without the required permission is denied; same-role callers outside resource scope are denied.
- Unapproved, malformed, rolled-back or expired policy snapshots cannot silently authorize work.
- A policy-management outage permits only explicitly valid last-known-good policy use; required fresh checks fail closed.
- Measured grant/revocation propagation includes JWT claim age and caches, not just policy publication time.
- No business request requires a private gateway or central policy round trip in the default deployment.

The reference directory preserves historical source documents; it is not an alternative to this accepted authorization decision. No application implementation or runtime test is claimed by this documentation change.
