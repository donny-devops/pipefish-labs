.PHONY: test verify-dom mcp compliance clean lint build health

test:
	python -m unittest discover -s tests -p "test_*.py" -v

verify-dom:
	python scripts/verify_dom_integrity.py

health:
	python scripts/health_check.py

mcp:
	python sdk/mcp_server.py

compliance:
	python sdk/cli.py compliance

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"

lint:
	python -m unittest discover -s tests

build:
	python -m build
