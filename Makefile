install:
	@echo "--- 🚀 Installing project dependencies ---"
	uv pip install -e ./browsergym/core -e ./browsergym/miniwob -e ./browsergym/webarena -e ./browsergym/visualwebarena/ -e ./browsergym/experiments -e ./browsergym/assistantbench -e ./browsergym/ -e ./browsergym/async_core/
	uv pip install -e ./browsergym/async_core/ -e ./browsergym/async_webarena/
	playwright install chromium

sync:
	uv pip install -e ./browsergym/core -e ./browsergym/miniwob -e ./browsergym/webarena -e ./browsergym/visualwebarena/ -e ./browsergym/experiments -e ./browsergym/assistantbench -e ./browsergym/
	playwright install chromium

async:
	uv pip install -e ./browsergym/async_core/ -e ./browsergym/async_webarena/
	playwright install chromium

install-demo:
	@echo "--- 🚀 Installing demo dependencies ---"
	uv pip install -r demo_agent/requirements.txt
	playwright install chromium

demo:
	@echo "--- 🚀 Running demo agent ---"
	(set -x && cd demo_agent && python run_demo.py)

test-core:
	@echo "--- 🧪 Running tests ---"
	pytest -n auto ./tests/core
