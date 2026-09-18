#!/usr/bin/env python3
"""Post the built requests to TypeSafe System One and record every response.

Stdlib only, like the rest of the pipeline. One result line per request:
the answers, token usage, wall-clock latency and how many attempts it took,
so a score can always be traced back to the exchange that produced it.

Resumable: ids already present in the output file are skipped, so a run
interrupted by a rate limit can simply be started again.

    export TYPESAFE_API_KEY=...
    python3 scripts/run_bench.py --requests data/requests/with_key.jsonl \
        --out data/results/with_key.jsonl

Retries follow the SDK's documented policy: 408, 429 and 5xx are retried with
exponential backoff and jitter, honouring Retry-After / retry-after-ms when the
server sends one; 400, 401, 403, 404 and 422 are permanent and stop that item.
"""

import argparse
import json
import os
import pathlib
import random
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _env  # noqa: E402  - local helper, no dependency

_env.load()

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = "https://api.typesafe.ai/v1/systemone"
RETRY_STATUS = {408, 429}
PERMANENT = {400, 401, 403, 404, 422}
PRINT_LOCK = threading.Lock()


def post(payload: dict, key: str, timeout: float, max_retries: int) -> tuple[dict, int, float]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    delay, started, attempt = 0.5, time.monotonic(), 0
    while True:
        attempt += 1
        req = urllib.request.Request(
            URL, data=body, method="POST",
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                out = json.loads(resp.read().decode("utf-8"))
            return out, attempt, (time.monotonic() - started) * 1000
        except urllib.error.HTTPError as e:
            status = e.code
            detail = e.read().decode("utf-8", "replace")[:400]
            if status in PERMANENT or attempt > max_retries:
                raise RuntimeError("HTTP %d after %d attempt(s): %s" % (status, attempt, detail))
            wait = None
            if status in RETRY_STATUS or 500 <= status < 600:
                for h in ("retry-after-ms", "Retry-After"):
                    v = e.headers.get(h)
                    if v:
                        try:
                            wait = float(v) / (1000 if h == "retry-after-ms" else 1)
                        except ValueError:
                            wait = None
                        break
            else:
                raise RuntimeError("HTTP %d: %s" % (status, detail))
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if attempt > max_retries:
                raise RuntimeError("connection failed after %d attempt(s): %s" % (attempt, e))
            wait = None
        if wait is None:
            wait = delay * (1 - random.random() * 0.25)
            delay = min(delay * 2, 5.0)
        time.sleep(wait)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--requests", default="data/requests/with_key.jsonl")
    ap.add_argument("--out", default="data/results/with_key.jsonl")
    ap.add_argument("--concurrency", type=int, default=int(os.environ.get("BENCH_CONCURRENCY", 4)))
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--max-retries", type=int, default=5)
    ap.add_argument("--limit", type=int, default=0, help="smoke test: only the first N requests")
    ap.add_argument("--dry-run", action="store_true", help="validate payloads, send nothing")
    args = ap.parse_args()

    rows = [json.loads(l) for l in (ROOT / args.requests).read_text(encoding="utf-8").splitlines() if l.strip()]
    if args.limit:
        rows = rows[: args.limit]

    out_path = ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out_path.exists():
        for line in out_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                done.add(json.loads(line)["id"])
    todo = [r for r in rows if r["id"] not in done]
    print("%d requests, %d already done, %d to send" % (len(rows), len(rows) - len(todo), len(todo)))

    if args.dry_run:
        for r in todo:
            p = r["payload"]
            assert p["questions"] and p["state"], r["id"]
            json.dumps(p, ensure_ascii=False)
        print("dry run ok: %d payloads well formed, nothing sent" % len(todo))
        return

    key = os.environ.get("TYPESAFE_API_KEY")
    if not key:
        sys.exit("TYPESAFE_API_KEY kosong. Isi di .env (lihat .env.example), "
                 "atau export TYPESAFE_API_KEY=..., atau jalankan dengan --dry-run.")

    fh = out_path.open("a", encoding="utf-8")
    write_lock = threading.Lock()
    failures = []

    def work(row: dict) -> None:
        try:
            answers, attempts, ms = post(row["payload"], key, args.timeout, args.max_retries)
            rec = {
                "id": row["id"], "subtest": row["subtest"], "type": row["type"],
                "answers": answers.get("answers", {}), "usage": answers.get("usage", {}),
                "model": answers.get("model"), "latency_ms": round(ms, 1), "attempts": attempts,
            }
            if "members" in row:
                rec["members"] = row["members"]
        except Exception as e:  # noqa: BLE001 - recorded, run continues
            rec = {"id": row["id"], "subtest": row["subtest"], "type": row["type"], "error": str(e)}
            failures.append(row["id"])
        with write_lock:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
        with PRINT_LOCK:
            mark = "!" if "error" in rec else "."
            print(mark, end="", flush=True)

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        list(pool.map(work, todo))
    fh.close()
    print()
    if failures:
        print("%d failed: %s" % (len(failures), ", ".join(failures[:10])), file=sys.stderr)
        print("re-run the same command to retry only those", file=sys.stderr)
    print("wrote %s" % out_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
