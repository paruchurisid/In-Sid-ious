from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from urllib.parse import urlparse
from services.orchestrator.demo_cycle import run_demo
from data.generator.swarm_telemetry import generate
from services.api.insights import insight, portfolio
app=FastAPI(title="Dual-Loop Retention Swarm")
app.mount("/assets", StaticFiles(directory=Path(__file__).parents[2] / "apps" / "control_room" / "dist" / "assets"), name="assets")
ALLOWED={"localhost","127.0.0.1"}
@app.get("/api/demo")
def demo(): return run_demo()
@app.get("/api/telemetry")
def telemetry():
 import json
 source=Path(__file__).parents[2] / "data" / "generated_swarm" / "accounts_telemetry.json"
 if not source.exists(): generate()
 return json.loads(source.read_text())
def _accounts(): return telemetry()
@app.get("/api/accounts/{account_id}")
def account_details(account_id:str):
 account=next((x for x in _accounts() if x["account_id"]==account_id),None)
 if not account: raise HTTPException(404,"Unknown account")
 return insight(account)
@app.get("/api/portfolio")
def portfolio_summary(): return portfolio(_accounts())
@app.get("/health")
def health(): return {"status":"ok","service":"retention-swarm","mode":"offline-deterministic"}
@app.get("/api/readiness")
def readiness():
 source=Path(__file__).parents[2] / "data" / "generated_swarm" / "accounts_telemetry.json"
 return {"ready":source.exists(),"telemetry_fixture":source.exists(),"demo":"deterministic","ui_bundle":(Path(__file__).parents[2] / "apps" / "control_room" / "dist" / "index.html").exists()}
@app.get("/")
def control_room(): return FileResponse(Path(__file__).parents[2] / "apps" / "control_room" / "dist" / "index.html")
@app.post("/api/test/reset")
def reset(account_id:str="all"):
 accounts,audits=generate()
 event_db=Path(__file__).parents[2] / "data" / "swarm_events.sqlite"
 if event_db.exists(): event_db.unlink()
 return {"account_id":account_id,"reset":True,"accounts":len(accounts),"audit_events":len(audits),"event_log_cleared":not event_db.exists(),"readiness":readiness()}
@app.get("/api/validate-target")
def validate_target(target_url:str):
 host=urlparse(target_url).hostname
 if host not in ALLOWED: raise HTTPException(403,"Target host is not in the sandbox allowlist")
 return {"allowed":True,"host":host}
