# 3-minute stage runbook

## Before walking on stage

1. Run `make stage-ready`.
2. Run `make api` in a dedicated terminal and wait for `Uvicorn running`.
3. Open `http://127.0.0.1:8000/`, press the **Full screen** button, and confirm the green `LIVE · deterministic run` badge.
4. Keep this terminal command ready for recovery: `Invoke-RestMethod -Method Post http://127.0.0.1:8000/api/test/reset`.

## Golden path

1. **0:00–0:35:** Point to Portfolio MASR and exposure mitigated. Select `acct_001 — Northstar Logistics`.
2. **0:35–1:15:** Explain paid seats versus active seats and the 20% utilization diagnosis.
3. **1:15–2:10:** Read the red baseline exploit, then follow the central patch operations to the green remediation outcome.
4. **2:10–2:45:** Move the persona slider to Discount Grifter and explain that the consultation rejects repeat discount farming.
5. **2:45–3:00:** Close on MASR moving from 0.8000 to 0.9500.

## Recovery

- If dashboard loading fails, refresh once. If still unavailable, run the reset command above and refresh.
- If the API is down, run `make api`; the app has no third-party runtime dependency.
- Use `/api/readiness` to confirm fixture and UI state.
