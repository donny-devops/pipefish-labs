.PHONY: test verify-dom mcp compliance clean lint build health build-site serve preview deploy

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

build-site:
	python scripts/build_site.py

serve: build-site
	python scripts/serve_preview.py --foreground

preview: build-site
	npx wrangler dev

deploy:
	npx wrangler deploy
