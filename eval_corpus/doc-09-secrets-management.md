# Secrets Management for Applications

Hardcoded credentials in source code are a frequent security weakness.

Safer approach:
- Store secrets in a dedicated vault service.
- Rotate credentials automatically and on incidents.
- Scope secret access to workload identity.

Operational notes:
- Avoid long-lived static API tokens.
- Audit secret reads and admin actions.
- Use environment injection carefully in CI/CD pipelines.

Good secrets hygiene limits the impact of repository leaks.
