# CLI Reference & Command Guide

[Overview](README.md) • [Getting Started](getting-started.md) • [Architecture](architecture.md) • [CLI Reference](usage.md) • [Configuration](configuration.md)

---

## Command Overview

```text
Usage: rime [options]
       rime <format> [options]
       rime undo [options]
       rime mcp
```

| Invocation | Description |
| :--- | :--- |
| `rime` | Interactive wizard: displays directory preview and prompts for target casing format. |
| `rime <format> [options]` | Batch rename target files using the chosen case transformation. |
| `rime undo [options]` | Revert previous batch rename operations from the transaction journal. |
| `rime mcp` | Launch standard I/O Model Context Protocol (MCP) server for agentic environments. |

---

## Case Transformation Modes

| Flag | Target Mode | Input Filename | Transformed Filename |
| :--- | :--- | :--- | :--- |
| `--title-snake` | `Title_Snake_Case` *(Default)* | `quarterly report 2024.pdf` | `Quarterly_Report_2024.pdf` |
| `--snake` | `snake_case` | `Quarterly Report 2024.pdf` | `quarterly_report_2024.pdf` |
| `--kebab` | `kebab-case` | `Quarterly Report 2024.pdf` | `quarterly-report-2024.pdf` |
| `--pascal` | `PascalCase` | `quarterly_report_2024.pdf` | `QuarterlyReport2024.pdf` |
| `--camel` | `camelCase` | `Quarterly_Report_2024.pdf` | `quarterlyReport2024.pdf` |
| `--upper-snake` | `UPPER_SNAKE_CASE` | `quarterly_report_2024.pdf` | `QUARTERLY_REPORT_2024.pdf` |
| `--lower` | `lowercase` | `Quarterly_Report_2024.PDF` | `quarterly_report_2024.pdf` |
| `--upper` | `UPPERCASE` | `quarterly report 2024.pdf` | `QUARTERLY REPORT 2024.pdf` |

---

## Options and Flags

| Flag | Long Option | Description | Default |
| :--- | :--- | :--- | :--- |
| `-d` | `--dir DIR` | Target directory to process. | Current directory (`.`) |
| `-e` | `--ext EXT` | Filter files by extension (e.g. `pdf`, `mp3`, `rs`). | All extensions (`*`) |
| `-r` | `--recursive` | Recursively scan and rename inside subdirectories. | `false` |
| | `--dirs` | Also rename matching directory names. | `false` |
| `-s` | `--safe` | Strict ASCII mode: strip accents (`é` $\to$ `e`) and special characters. | `false` |
| `-a` | `--all`, `--hidden` | Include hidden dotfiles (hard-excludes `.git`). | `false` |
| `-l` | `--lower-ext` | Normalize file extensions to lowercase (`.PDF` $\to$ `.pdf`). | `true` |
| | `--no-lower-ext` | Preserve existing extension casing. | `false` |
| `-n` | `--dry-run` | Preview planned renames without modifying disk state. | `false` |
| `-y` | `--yes` | Skip interactive confirmation and apply renames immediately. | `false` |
| | `--conflict MODE` | Conflict handling strategy: `skip`, `suffix`, or `abort`. | `skip` |
| `-A` | `--agent` | Compact machine-readable output mode for agents. | `false` |
| | `--json` | Output execution results in structured JSON format. | `false` |
| | `--color MODE` | Terminal color mode: `auto`, `always`, or `never`. | `auto` |
| | `--no-color` | Disable colored terminal output. | `false` |
| `-h` | `--help` | Show command-line help text. | - |
| `-V` | `--version` | Display version information. | - |

---

## Undo and History

Every executed batch operation writes a recovery manifest to `$XDG_CACHE_HOME/rime/undo.json`.

### Reverting the Last Operation

```bash
rime undo
```

### Simulating an Undo Operation

To preview what files will be reverted without moving them:

```bash
rime undo --dry-run
```

### Inspecting Previous Operations

To review historical rename logs recorded in the transaction journal:

```bash
rime undo --list
# or alias:
rime log
```

---

## MCP Server

Rime exposes a native Model Context Protocol (MCP) server over standard I/O:

```bash
rime mcp
```

### MCP Tools Exposed

1. **`rime_rename`**: Execute atomic batch rename with specified case mode and options.
2. **`rime_preview`**: Scan directory and return planned renames without disk writes.
3. **`rime_undo`**: Revert the previous batch rename operation.
4. **`rime_list_history`**: List historical rename operations stored in the cache journal.

### MCP Client Configuration

Add Rime to your MCP client configuration (e.g. `~/.gemini/config/mcp_config.json`):

```json
{
  "mcpServers": {
    "rime": {
      "command": "rime",
      "args": ["mcp"]
    }
  }
}
```

---

## Practical Recipes

### Recipe 1: Normalize Asset Names in a Web Project

Convert images and SVG assets to kebab-case with lowercase extensions:

```bash
rime --kebab -r -e svg --dir public/assets/
rime --kebab -r -e png --dir public/assets/
```

### Recipe 2: Clean Downloaded Course Files

Strip accents, eliminate spaces, and standardize documents to Title_Snake_Case:

```bash
rime --title-snake -s -e pdf --dir ~/Downloads/
```

### Recipe 3: Automated Pipeline Renaming

In scripts where interaction is not possible, use non-interactive mode with JSON output:

```bash
rime --snake -y --json -r -d ./output
```
