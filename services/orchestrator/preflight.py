"""Stage preflight: checks local API latency and compiled dashboard availability."""
from urllib.request import urlopen
from time import perf_counter
def main():
    for route in ("/health","/api/readiness","/api/portfolio","/"):
        start=perf_counter()
        with urlopen("http://127.0.0.1:8000"+route,timeout=3) as r: assert r.status==200
        elapsed=(perf_counter()-start)*1000
        if elapsed>1000: raise SystemExit(f"PREFLIGHT FAILED: {route} took {elapsed:.0f}ms")
        print(f"OK {route}: {elapsed:.0f}ms")
    print("PREFLIGHT PASS")
if __name__=="__main__": main()
