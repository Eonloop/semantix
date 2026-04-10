# Evaluation Queries and Relevance Labels

Use this file to evaluate MRR and Recall@K.

## Query Set

1. Query: "how to prevent sql injection in authentication systems"
   - Relevant docs: `doc-01-sql-injection.md`

2. Query: "ways to stop script injection in user comments"
   - Relevant docs: `doc-02-cross-site-scripting.md`

3. Query: "steps for ransomware containment and recovery"
   - Relevant docs: `doc-03-ransomware-response.md`

4. Query: "zero trust access principles and microsegmentation"
   - Relevant docs: `doc-04-zero-trust-networking.md`

5. Query: "sbom usage for vulnerability impact analysis"
   - Relevant docs: `doc-05-sbom-supply-chain.md`

6. Query: "api throttling and token bucket strategy"
   - Relevant docs: `doc-06-api-rate-limiting.md`

7. Query: "how to reduce phishing risk in enterprise email"
   - Relevant docs: `doc-07-phishing-defense.md`

8. Query: "container runtime hardening and non-root execution"
   - Relevant docs: `doc-08-container-hardening.md`

9. Query: "vault-based secret rotation best practices"
   - Relevant docs: `doc-09-secrets-management.md`

10. Query: "defending web services against ddos traffic floods"
   - Relevant docs: `doc-10-ddos-resilience.md`

## Notes

- Start with `K = 1, 3, 5`.
- Track both exact-match queries and paraphrased variants.
- Add 2-3 multi-relevant queries once your index grows (one query mapping to multiple relevant docs).
