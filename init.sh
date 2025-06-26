pip install uv
uv venv
source .venv/bin/activate
uv pip compile pyproject.toml >requirements.txt
uv pip install -r requirements.txt
