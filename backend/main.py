"""PromptLab API Server

Run with: python main.py
"""

import os

import uvicorn
from app.api import app


def _env_flag(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).lower() in {"1", "true", "yes", "on"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    reload_enabled = _env_flag("UVICORN_RELOAD", "false")
    uvicorn.run("app.api:app", host="0.0.0.0", port=port, reload=reload_enabled)

