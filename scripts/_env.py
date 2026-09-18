"""Tiny .env reader so the scripts pick the key up without a dependency.

Real environment variables always win: exporting TYPESAFE_API_KEY overrides
whatever the file says.
"""

import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load(path: str = ".env") -> None:
    f = ROOT / path
    if not f.exists():
        return
    for raw in f.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip("'\"")
        if k and v and k not in os.environ:
            os.environ[k] = v
