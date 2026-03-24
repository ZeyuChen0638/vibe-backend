import os
import subprocess
import sys
from pathlib import Path
import argparse

import uvicorn


APP_IMPORT = "app.main:app"
ROOT = Path(__file__).resolve().parent


def _port(default: int = 8000) -> int:
    return int(os.getenv("PORT", str(default)))


def _run(*args: str) -> None:
    subprocess.run([sys.executable, "-m", "alembic", *args], check=True, cwd=ROOT)


def dev() -> None:
    subprocess.run(["fastapi", "dev", "app/main.py", "--host", "127.0.0.1", "--port", "8000"], check=True)


def start() -> None:
    uvicorn.run(
        APP_IMPORT,
        host=os.getenv("HOST", "0.0.0.0"),
        port=_port(),
        reload=False,
    )


def db() -> None:
    parser = argparse.ArgumentParser(prog="db", description="Run Alembic database commands")
    subparsers = parser.add_subparsers(dest="command", required=True)

    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade to a migration revision")
    upgrade_parser.add_argument("revision", nargs="?", default="head")

    downgrade_parser = subparsers.add_parser("downgrade", help="Downgrade to a migration revision")
    downgrade_parser.add_argument("revision", nargs="?", default="-1")

    revision_parser = subparsers.add_parser("revision", help="Create a new migration revision")
    revision_parser.add_argument("-m", "--message", required=True)
    revision_parser.add_argument("--autogenerate", action="store_true")

    subparsers.add_parser("current", help="Show the current revision")
    subparsers.add_parser("history", help="Show migration history")

    stamp_parser = subparsers.add_parser("stamp", help="Stamp the database with a revision")
    stamp_parser.add_argument("revision", nargs="?", default="head")

    args = parser.parse_args()

    if args.command == "upgrade":
        _run("upgrade", args.revision)
    elif args.command == "downgrade":
        _run("downgrade", args.revision)
    elif args.command == "revision":
        revision_args = ["revision", "-m", args.message]
        if args.autogenerate:
            revision_args.insert(1, "--autogenerate")
        _run(*revision_args)
    elif args.command == "current":
        _run("current")
    elif args.command == "history":
        _run("history")
    elif args.command == "stamp":
        _run("stamp", args.revision)
