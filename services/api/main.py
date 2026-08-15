from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from urllib.parse import urlparse
from services.orchestrator.demo_cycle import run_demo
app=FastAPI(title="Dual-Loop Retention Swarm")
app.mount("/assets", StaticFiles(directory=Path(__file__).parents[2] / "apps" / "control_room" / "dist" / "assets"), name="assets")
ALLOWED={"localhost","127.0.0.1"}
@app.get("/api/demo")
def demo(): return run_demo()
@app.get("/api/telemetry")
def telemetry():
 import json
 return json.loads((Path(__file__).parents[2] / "data" / "generated_swarm" / "accounts_telemetry.json").read_text())
@app.get("/")
def control_room(): return FileResponse(Path(__file__).parents[2] / "apps" / "control_room" / "dist" / "index.html")
@app.post("/api/test/reset")
def reset(account_id:str): return {"account_id":account_id,"reset":True}
@app.get("/api/validate-target")
def validate_target(target_url:str):
 host=urlparse(target_url).hostname
 if host not in ALLOWED: raise HTTPException(403,"Target host is not in the sandbox allowlist")
 return {"allowed":True,"host":host}
