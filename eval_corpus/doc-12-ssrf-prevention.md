# Server-Side Request Forgery Mitigation

Server-side request forgery (SSRF) occurs when an attacker manipulates a server into making requests to unintended internal or external destinations.

Common vectors:
- URL parameters passed directly to backend HTTP clients.
- PDF generators or webhook integrations that fetch user-supplied URLs.
- Cloud metadata endpoints accessible from application hosts.

Potential impact:
- Exposure of internal service responses and cloud instance credentials.
- Port scanning and service discovery within private networks.
- Bypassing network-level access controls through the trusted server.

Recommended controls:
- Allowlist permitted destination hosts and schemas.
- Block requests to private IP ranges and link-local addresses.
- Run outbound fetches in isolated network segments with egress filtering.

SSRF risk increases in cloud environments where metadata services return temporary credentials.
