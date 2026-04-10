# API Rate Limiting Strategies

Rate limiting helps protect APIs from abuse and accidental overload.

Typical patterns:
- Fixed window limits per API key.
- Token bucket for burst tolerance.
- Sliding window for smoother enforcement.

Design considerations:
- Return clear 429 responses and retry headers.
- Separate limits by endpoint sensitivity.
- Monitor false positives for legitimate clients.

Rate limiting is stronger when combined with authentication and bot detection.
