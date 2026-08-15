# Dual-Loop Retention Swarm

Offline, deterministic retention-loop demo. Run `python -m pip install -e .`, then `make demo-cycle` (or `python -m services.orchestrator.demo_cycle`).

The demo creates an at-risk cohort, derives a persona, audits a deliberately vulnerable offer policy, proposes a tighten-only patch, replays the same persona, and reports the MASR change. `make test` validates contract propagation, policy guardrails, economics, and host allowlisting.
