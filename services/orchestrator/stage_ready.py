"""One-command local rehearsal validation and T-0 reset."""
import subprocess, sys
from pathlib import Path
from data.generator.swarm_telemetry import generate
from services.orchestrator.demo_cycle import run_demo
def main():
    root=Path(__file__).parents[2]
    generate(); result=subprocess.run([sys.executable,"-m","pytest","-q"],cwd=root,check=False)
    if result.returncode: raise SystemExit(result.returncode)
    demo=run_demo()
    if not demo["improved"] or demo["masr_after"] != "0.9500": raise SystemExit("Golden-path verification failed")
    print("STAGE READY: fixtures reset, tests passed, deterministic replay verified. Start: make api")
if __name__=="__main__": main()
