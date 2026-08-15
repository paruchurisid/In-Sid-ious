# Dual-Loop Retention Swarm

Dual-Loop Retention Swarm is an offline, deterministic demonstration of an AI-assisted customer-retention system. It turns account telemetry into a repeatable closed loop: identify risk, understand unrealized value, test a retention policy against an adversarial persona, and safely tighten the policy when the test exposes an exploit.

The project makes the operational decisions inspectable. It is not connected to a CRM, billing provider, or production model endpoint.

## What the system does

For each account, the system evaluates recent seat activity, feature adoption, health signals, and MRR. It then provides an account-specific view of:

- Entitlement realization — the share of paid seats that are active.
- At-risk MRR — the account's monthly recurring revenue when its health state is critical, high, or watch.
- Exposure mitigated — estimated annualized margin protected by an approved autonomous policy change.
- Autonomous patches — whether the selected account received a safe policy patch.

Changing the selected account in the control room calls the account-insight API again. The UI refreshes its metrics, remediation inspector, and persona replay for that account rather than showing portfolio-level constants.

## The two loops

### 1. Value-realization loop

1. The Dormancy Watchdog scores account health and creates an at-risk cohort.
2. The Value Realization Agent compares purchased capacity and entitlements with actual use, identifies unused high-value features, and recommends right-sizing, onboarding, or support escalation.
3. The control room presents utilization, ROI gap, churn probability, and MRR at risk for the account.

### 2. Policy-safety loop

1. The Persona Generator creates a representative cancellation or negotiation persona.
2. The mock Sirius adapter runs that persona through the current retention-offer policy.
3. The Exploit Auditor identifies unsafe concessions, such as an uncapped discount that can be repeatedly exploited.
4. The Policy Synthesizer applies only tighten-only operations: lower a discount ceiling, shorten duration, add a cooldown, or replace a monetary offer with a value-recovery action.
5. The same persona is replayed against the patched policy and the Margin-Adjusted Save Rate (MASR) is compared before and after.

Accounts without a detected policy exploit remain under monitoring and show no autonomous deployment. This distinguishes a genuine remediation from an account that needs adoption work or human attention.

## Repository layout

| Path | Purpose |
| --- | --- |
| `agents/` | Deterministic implementations of the watchdog, value, persona, and exploit-auditor agents. |
| `services/orchestrator/` | Runs the end-to-end closed-loop demonstration. |
| `services/policy_engine/` | Enforces and applies retention-offer policy patches. |
| `services/api/` | FastAPI endpoints for telemetry, portfolio summaries, account-specific insights, and the control room. |
| `apps/control_room/` | React/Vite dashboard for inspecting account telemetry and agent decisions. |
| `data/generator/` | Generates the ten-account, 90-day deterministic telemetry fixture. |
| `packages/contracts/` | Shared Pydantic contracts passed between agents and services. |
| `tests/` | Contract, economics, policy, API, and account-insight tests. |

## Run it locally

Install the Python package:

```bash
python -m pip install -e .
```

Generate the deterministic telemetry fixture and run the agent loop:

```bash
make generate
make demo-cycle
```

Start the API and control room at `http://127.0.0.1:8000`:

```bash
make api
```

Build the dashboard after UI changes:

```bash
make ui-build
```

Run the automated checks:

```bash
make test
```

## Important implementation note

“AI agents” in this repository currently means deterministic, inspectable agent logic and simulated persona replays. That makes the demo stable and safe for local evaluation. Replacing the deterministic implementations with live model calls, real telemetry ingestion, identity controls, audit storage, and approval workflows would be required before using it for production retention decisions.
