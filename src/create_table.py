from __future__ import annotations

import argparse
import gzip
import json
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq
from tqdm import tqdm


def safe_get(d: dict[str, Any] | None, *keys: str) -> Any:
    cur = d
    for key in keys:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


SCHEMA = pa.schema(
    [
        ("event_id", pa.string()),
        ("event_type", pa.string()),
        ("is_public", pa.bool_()),
        ("created_at", pa.string()),
        ("actor_id", pa.int64()),
        ("actor_login", pa.string()),
        ("actor_display_login", pa.string()),
        ("repo_id", pa.int64()),
        ("repo_name", pa.string()),
        ("org_id", pa.int64()),
        ("org_login", pa.string()),
        ("payload_json", pa.string()),
        ("source_file", pa.string()),
    ]
)


def event_to_row(event: dict[str, Any], source_file: str) -> dict[str, Any]:
    payload = event.get("payload")

    return {
        "event_id": str(event.get("id")) if event.get("id") is not None else None,
        "event_type": event.get("type"),
        "is_public": event.get("public"),
        "created_at": event.get("created_at"),
        "actor_id": safe_get(event, "actor", "id"),
        "actor_login": safe_get(event, "actor", "login"),
        "actor_display_login": safe_get(event, "actor", "display_login"),
        "repo_id": safe_get(event, "repo", "id"),
        "repo_name": safe_get(event, "repo", "name"),
        "org_id": safe_get(event, "org", "id"),
        "org_login": safe_get(event, "org", "login"),
        "payload_json": json.dumps(payload, ensure_ascii=False) if payload is not None else None,
        "source_file": source_file,
    }


def flush_batch(rows: list[dict[str, Any]], writer: pq.ParquetWriter) -> None:
    if not rows:
        return

    columns = {name: [row.get(name) for row in rows] for name in SCHEMA.names}
    table = pa.Table.from_pydict(columns, schema=SCHEMA)
    writer.write_table(table)


def convert(input_dir: Path, output_path: Path, batch_size: int, limit_files: int | None) -> None:
    files = sorted(input_dir.glob("*.json.gz"))

    if limit_files is not None:
        files = files[:limit_files]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = pq.ParquetWriter(
        where=output_path,
        schema=SCHEMA,
        compression="zstd",
        use_dictionary=True,
    )

    rows: list[dict[str, Any]] = []
    total_events = 0
    bad_lines = 0

    try:
        for path in tqdm(files, desc="Converting files"):
            with gzip.open(path, "rt", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        bad_lines += 1
                        continue

                    rows.append(event_to_row(event, source_file=path.name))
                    total_events += 1

                    if len(rows) >= batch_size:
                        flush_batch(rows, writer)
                        rows.clear()

        flush_batch(rows, writer)

    finally:
        writer.close()

    print(f"Written: {output_path}")
    print(f"Files processed: {len(files)}")
    print(f"Events processed: {total_events}")
    print(f"Bad JSON lines: {bad_lines}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("data/events.parquet"))
    parser.add_argument("--batch-size", type=int, default=50_000)
    parser.add_argument("--limit-files", type=int, default=None)

    args = parser.parse_args()

    convert(
        input_dir=args.input_dir,
        output_path=args.output,
        batch_size=args.batch_size,
        limit_files=args.limit_files,
    )


if __name__ == "__main__":
    main()
