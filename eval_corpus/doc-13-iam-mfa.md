# Identity and Access Management with MFA

Identity and access management (IAM) controls who can access resources and under what conditions. Multi-factor authentication (MFA) adds a critical layer beyond passwords.

IAM fundamentals:
- Enforce least privilege through role-based access control.
- Use federated identity providers to centralize authentication.
- Review and recertify access grants on a regular schedule.

MFA deployment:
- Require MFA for all privileged and remote access accounts.
- Prefer phishing-resistant methods like FIDO2 hardware keys.
- Provide fallback recovery flows that do not weaken the overall security posture.

Monitoring and response:
- Alert on impossible-travel logins and credential stuffing patterns.
- Automatically step up authentication for anomalous sessions.
- Log all authentication events for audit and forensic review.

Strong IAM with enforced MFA significantly reduces the risk of credential-based account takeover.
