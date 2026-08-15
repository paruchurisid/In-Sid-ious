# Decisions

- **Sirius integration:** no Sirius API credentials or write-access documentation were supplied. The application defaults to `MockSiriusClient`; a live client must remain read-only until programmatic write access is independently verified.
- **Demo scope:** the system is offline and deterministic (`SWARM_SEED=42`), using generated cohort data and rule-based stand-ins where an external LLM/browser would otherwise be required.
