.PHONY: test demo demo-cycle generate api ui-build stage-ready preflight
test:
	python -m pytest -q
generate:
	python -m data.generator.swarm_telemetry
ui-build:
	pnpm --dir apps/control_room build
stage-ready: ui-build
	python -m services.orchestrator.stage_ready
preflight:
	python -m services.orchestrator.preflight
demo demo-cycle:
	python -m services.orchestrator.demo_cycle
api:
	python -m uvicorn services.api.main:app --reload
