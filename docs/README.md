<p align="center">
  <img src="assets/banner.png" alt="Delicate rime ice needle crystals formed by freezing supercooled fog" width="100%" />
</p>

# Rime 🔤

[Overview](README.md) • [Getting Started](getting-started.md) • [Architecture](architecture.md) • [CLI Reference](usage.md) • [Configuration](configuration.md)

---

> Universal filename sanitizer, Unicode accent normalizer, and batch renaming engine with instant transaction rollback.

Rime standardizes project naming conventions, decomposes diacritics, and normalizes casing across directories and file hierarchies. It handles multi-word tokenization, collision avoidance, and maintains an atomic transaction journal for single-command rollback.

---

## Why "Rime"? (The Lore)

> **rime** (`/raɪm/`) — *noun:* A crystalline crust of ice formed when supercooled fog droplets freeze instantly upon contacting exposed surfaces, encasing irregular shapes in smooth, uniform white shells.

In subzero coastal air, jagged rocks, rough wire fences, and weather-beaten timber are steadily coated in rime—smoothed out and regularized into clean, unified crystalline forms. 

Project directories frequently mirror that jagged landscape: spaces mixed with underscores, erratic capitalizations, accented characters, and mismatched file extensions.

**Rime encases uneven filesystems in clean conventions:**

- **Surface Regularization**: Scans directories to sanitize erratic whitespace, special punctuation, and mixed casing into consistent, predictable naming conventions.
- **Deterministic Transformations**: Supports eight distinct casing formats, Unicode NFKD diacritic normalization, dry-run simulations, and transaction-logged rollback.

---

## Architecture at a Glance

Rime is structured into five core modules:

1. **Tokenization & Transformation (`rime.transform`)**: Word-boundary regex tokenizers, Unicode NFKD decomposition, and format casing formatters.
2. **Rename Engine (`rime.engine`)**: Filesystem scanner, bottom-up tree traversal, and collision detection (`skip`, `suffix`, `abort`).
3. **History & Rollback (`rime.history`)**: JSON transaction journal storing previous renames for 1-command atomic rollback.
4. **CLI Harness & Dispatcher (`rime.cli`)**: Flag parsing, interactive wizard, and machine-readable output formatting.
5. **Model Context Protocol (`rime.mcp`)**: Stdio server exposing atomic renaming, previewing, and rollback tools to agentic environments.

---

## Supported Case Transformations

| Flag | Format Name | Example Transformation |
| :--- | :--- | :--- |
| `--title-snake` | `Title_Snake_Case` *(Default)* | `annual report 2024.pdf` $\to$ `Annual_Report_2024.pdf` |
| `--snake` | `snake_case` | `annual report 2024.pdf` $\to$ `annual_report_2024.pdf` |
| `--kebab` | `kebab-case` | `annual report 2024.pdf` $\to$ `annual-report-2024.pdf` |
| `--pascal` | `PascalCase` | `annual report 2024.pdf` $\to$ `AnnualReport2024.pdf` |
| `--camel` | `camelCase` | `annual report 2024.pdf` $\to$ `annualReport2024.pdf` |
| `--upper-snake` | `UPPER_SNAKE_CASE` | `annual report 2024.pdf` $\to$ `ANNUAL_REPORT_2024.pdf` |
| `--lower` | `lowercase` | `Annual_Report_2024.PDF` $\to$ `annual_report_2024.pdf` |
| `--upper` | `UPPERCASE` | `annual report 2024.pdf` $\to$ `ANNUAL REPORT 2024.pdf` |

---

## Documentation Navigation

- [Installation & Quick Start](getting-started.md): How to install Rime via Nix, Home Manager, or pip, and quick examples.
- [Architecture & Design Philosophy](architecture.md): Word boundary tokenization, accent decomposition, bottom-up directory ordering, and collision safety.
- [CLI Reference & Command Guide](usage.md): Full flag specifications, undo workflows, MCP server instructions, and practical recipes.
- [Configuration & Advanced Options](configuration.md): Declarative configuration via `rime.toml` and Nix home manager modules.
