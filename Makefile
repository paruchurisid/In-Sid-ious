.PHONY: test demo demo-cycle generate api
test:
	python -m pytest -q
generate:
	python -m data.generator.generate
demo demo-cycle:
	python -m services.orchestrator.demo_cycle
api:
	python -m uvicorn services.api.main:app --reload
