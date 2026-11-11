"""Unit tests for Rime Model Context Protocol (MCP) server."""

from __future__ import annotations

import json
from pathlib import Path

from rime.mcp import StdioMCPServer, execute_tool


def test_mcp_initialize() -> None:
    server = StdioMCPServer()
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-agent", "version": "1.0"},
        },
    }
    resp = server.handle_request(req)
    assert resp is not None
    assert resp["id"] == 1
    assert resp["result"]["serverInfo"]["name"] == "rime"
    assert resp["result"]["protocolVersion"] == "2024-11-05"


def test_mcp_tools_list() -> None:
    server = StdioMCPServer()
    req = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    resp = server.handle_request(req)
    assert resp is not None
    tools = resp["result"]["tools"]
    tool_names = [t["name"] for t in tools]
    assert "rime_rename" in tool_names

    tool = next(t for t in tools if t["name"] == "rime_rename")
    props = tool["inputSchema"]["properties"]
    assert "path" in props
    assert "format" in props
    assert "ext" in props
    assert "recursive" in props
    assert "safe" in props
    assert "dry_run" in props


def test_mcp_ping() -> None:
    server = StdioMCPServer()
    req = {"jsonrpc": "2.0", "id": 3, "method": "ping"}
    resp = server.handle_request(req)
    assert resp == {"jsonrpc": "2.0", "id": 3, "result": {}}


def test_mcp_unknown_method() -> None:
    server = StdioMCPServer()
    req = {"jsonrpc": "2.0", "id": 4, "method": "unknown/method"}
    resp = server.handle_request(req)
    assert resp is not None
    assert "error" in resp
    assert resp["error"]["code"] == -32601


def test_execute_rime_rename_dry_run(tmp_path: Path) -> None:
    f1 = tmp_path / "hello world file.txt"
    f1.write_text("sample content")

    res = execute_tool(
        "rime_rename",
        {
            "path": str(tmp_path),
            "format": "title-snake",
            "dry_run": True,
        },
    )
    assert res["status"] == "ok"
    assert res["dry_run"] is True
    assert res["count"] == 1
    assert res["renamed"] == 0
    assert len(res["plans"]) == 1
    assert res["plans"][0]["relative_new"] == "Hello_World_File.txt"
    # Original file should still exist (dry run)
    assert f1.exists()


def test_execute_rime_rename_live(tmp_path: Path) -> None:
    f1 = tmp_path / "my document 123.pdf"
    f1.write_text("pdf bytes")

    res = execute_tool(
        "rime_rename",
        {
            "path": str(tmp_path),
            "format": "kebab",
            "dry_run": False,
        },
    )
    assert res["status"] == "ok"
    assert res["dry_run"] is False
    assert res["renamed"] == 1
    assert not f1.exists()
    renamed = tmp_path / "my-document-123.pdf"
    assert renamed.exists()


def test_execute_rime_rename_invalid_dir() -> None:
    res = execute_tool(
        "rime_rename",
        {
            "path": "/nonexistent/directory/path/here",
            "format": "snake",
        },
    )
    assert res["status"] == "error"
    assert "Directory not found" in res["error"]


def test_execute_unknown_tool() -> None:
    res = execute_tool("unknown_tool", {})
    assert res["status"] == "error"
    assert "Unknown tool" in res["error"]


def test_mcp_tools_call_handler(tmp_path: Path) -> None:
    server = StdioMCPServer()
    f = tmp_path / "another test.txt"
    f.write_text("text")

    req = {
        "jsonrpc": "2.0",
        "id": 10,
        "method": "tools/call",
        "params": {
            "name": "rime_rename",
            "arguments": {
                "path": str(tmp_path),
                "format": "snake",
                "dry_run": True,
            },
        },
    }
    resp = server.handle_request(req)
    assert resp is not None
    assert resp["id"] == 10
    content = resp["result"]["content"]
    assert len(content) == 1
    assert content[0]["type"] == "text"
    parsed = json.loads(content[0]["text"])
    assert parsed["status"] == "ok"
    assert parsed["format"] == "snake"
