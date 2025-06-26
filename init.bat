pip install uv
uv venv
call .venv\Scripts\activate
uv pip compile pyproject.toml > requirements.txt
uv pip install -r requirements.txt
