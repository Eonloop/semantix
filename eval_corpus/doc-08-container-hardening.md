# Container Hardening Best Practices

Containers reduce deployment friction but do not remove security responsibilities.

Hardening priorities:
- Use minimal base images.
- Run processes as non-root users.
- Keep images patched and rebuilt frequently.

Runtime controls:
- Read-only root filesystem where possible.
- Drop unnecessary Linux capabilities.
- Restrict network egress by policy.

Image scanning plus runtime monitoring gives better coverage than either alone.
