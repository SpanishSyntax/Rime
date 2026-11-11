"""Model Context Protocol (MCP) stdio server for Rime."""

from __future__ import annotations

import contextlib
import json
import sys
from pathlib import Path
from typing import Any

from rime import __version__
from rime.engine import execute_renames, resolve_conflicts, scan_directory

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "rime_rename",
        "description": "Batch sanitizes and case-transforms filenames across a directory using Rime.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Target directory to rename files in (default: .)",
                    "default": ".",
                },
                "format": {
                    "type": "string",
                    "description": "Target casing format: title-snake, snake, kebab, pascal, camel, lower, upper, upper-snake (default: title-snake)",
                    "default": "title-snake",
                },
                "ext": {
                    "type": "string",
                    "description": "Optional file extension filter (e.g. 'pdf', 'mp3') (default: '')",
                    "default": "",
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Recursively process subdirectories (default: True)",
                    "default": True,
                },
                "safe": {
                    "type": "boolean",
                    "description": "Strict ASCII mode: strip accents and special characters (default: True)",
                    "default": True,
                },
                "dry_run": {
                    "type": "boolean",
                    "description": "Preview planned renames without executing them (default: False)",
                    "default": False,
                },
            },
        },
    }
]


def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Execute a Rime MCP tool call and return JSON-serializable results."""
    try:
        if name == "rime_rename":
            raw_path = arguments.get("path", ".")
            raw_fmt = arguments.get(
                "format",
                arguments.get("case", arguments.get("case_mode", "title-snake")),
            )
            ext = arguments.get("ext", arguments.get("extension", ""))
            recursive = bool(arguments.get("recursive", True))
            safe = bool(arguments.get("safe", arguments.get("safe_ascii", True)))
            dry_run = bool(arguments.get("dry_run", False))

            target_dir = Path(raw_path).expanduser().resolve()
            if not target_dir.exists():
                return {
                    "status": "error",
                    "error": f"Directory not found: {target_dir}",
                }
            if not target_dir.is_dir():
                return {
                    "status": "error",
                    "error": f"Path is not a directory: {target_dir}",
                }

            case_mode = str(raw_fmt).strip().lower().replace("-", "_")
            valid_cases = {
                "title_snake",
                "snake",
                "kebab",
                "pascal",
                "camel",
                "lower",
                "upper",
                "upper_snake",
            }
            if case_mode not in valid_cases:
                case_mode = "title_snake"

            # Execute with stdout redirected to stderr to prevent stream corruption
            with contextlib.redirect_stdout(sys.stderr):
                plans = scan_directory(
                    root=target_dir,
                    extension=ext if ext else "*",
                    case_mode=case_mode,
                    safe_ascii=safe,
                    lower_ext=True,
                    recursive=recursive,
                    include_dirs=False,
                    include_hidden=False,
                )

                executable_plans, collisions = resolve_conflicts(
                    plans=plans,
                    on_conflict="skip",
                    target_dir=target_dir,
                )

                if not dry_run and executable_plans:
                    execute_renames(executable_plans)

            return {
                "status": "ok",
                "target_dir": str(target_dir),
                "format": case_mode,
                "dry_run": dry_run,
                "count": len(plans),
                "renamed": len(executable_plans) if not dry_run else 0,
                "collisions_count": len(collisions),
                "plans": [
                    {
                        "old": str(p.original),
                        "new": str(p.new_path),
                        "relative_old": p.relative_old,
                        "relative_new": p.relative_new,
                        "is_dir": p.is_dir,
                        "collision": p in collisions,
                    }
                    for p in plans
                ],
            }
        else:
            return {"status": "error", "error": f"Unknown tool: {name}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


class StdioMCPServer:
    """JSON-RPC 2.0 stdio server implementing the Model Context Protocol."""

    def __init__(self) -> None:
        self.server_info = {"name": "rime", "version": __version__}

    def handle_request(self, req: dict[str, Any]) -> dict[str, Any] | None:
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": self.server_info,
                    "capabilities": {"tools": {}},
                },
            }

        elif method == "notifications/initialized":
            return None

        elif method == "ping":
            return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {"tools": TOOL_DEFINITIONS},
            }

        elif method == "tools/call":
            params = req.get("params", {})
            name = params.get("name", "")
            args = params.get("arguments", {})
            res = execute_tool(name, args)
            is_error = res.get("status") == "error"

            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(res, indent=2)}],
                    "isError": is_error,
                },
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

    def run(self) -> None:
        """Run JSON-RPC event loop reading lines from sys.stdin."""
        for line in sys.stdin:
            line_str = line.strip()
            if not line_str:
                continue
            try:
                req = json.loads(line_str)
                resp = self.handle_request(req)
                if resp is not None:
                    sys.stdout.write(json.dumps(resp) + "\n")
                    sys.stdout.flush()
            except Exception as e:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {e}"},
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()
