# Cross-Site Scripting in Comment Widgets

Cross-site scripting (XSS) happens when untrusted content is rendered as executable script in a browser.

Common vectors:
- User comments rendered without escaping.
- DOM updates using unsafe HTML insertion APIs.

Impact examples:
- Session token theft.
- Defacement of visible page content.
- Malicious actions executed in user context.

Mitigation:
- Context-aware output encoding.
- Input sanitization for rich text.
- Content Security Policy (CSP) with nonce or hashes.
