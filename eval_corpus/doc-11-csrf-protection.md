# Cross-Site Request Forgery Prevention

Cross-site request forgery (CSRF) tricks authenticated users into submitting unintended state-changing requests to a web application.

Attack prerequisites:
- Victim has an active session with the target site.
- Target endpoint accepts state-changing requests without origin verification.
- Attacker can lure the victim to a crafted page or link.

Potential impact:
- Unauthorized fund transfers or account changes.
- Password or email address modification without user consent.
- Administrative actions performed under a hijacked session.

Recommended controls:
- Synchronizer token pattern with per-session CSRF tokens.
- SameSite cookie attribute set to Lax or Strict.
- Origin and Referer header validation on state-changing endpoints.

CSRF defenses are most effective when layered with proper session management and short-lived tokens.
