# SBOM and Software Supply Chain Security

A Software Bill of Materials (SBOM) lists components used by an application.

Why teams use SBOM:
- Faster impact analysis for new CVEs.
- Better dependency inventory across services.
- Improved compliance reporting.

Practical workflow:
- Generate SBOMs in CI for every build artifact.
- Track package versions and transitive dependencies.
- Map vulnerabilities to affected deployments.

SBOM data is most useful when tied to active asset inventories.
