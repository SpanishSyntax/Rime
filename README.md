<p align="center">
  <img src="assets/banner.png" alt="Delicate rime ice needle crystals formed by freezing supercooled fog" width="100%" />
</p>

# Rime 🔤

Universal filename sanitizer, Unicode accent normalizer, and batch renaming engine with instant transaction rollback.

Rime is a fast, non-destructive utility designed to normalize irregular filenames, decompose diacritics, and enforce consistent casing conventions across directories and project hierarchies.

---

> [!TIP]
> **Documentation Site**: Detailed transformation rules, tokenization algorithms, and configuration examples are available on the **[Documentation Site](https://spanishsyntax.github.io/Rime)**.

---

## Why "Rime"? (The Lore)

> **rime** (`/raɪm/`) — *noun:* A crystalline crust of ice formed when supercooled fog droplets freeze instantly upon contacting exposed surfaces, encasing irregular shapes in smooth, uniform white shells.

In subzero coastal air, jagged rocks, rough wire fences, and weather-beaten timber are steadily coated in rime—smoothed out and regularized into clean, unified crystalline forms.

Project directories frequently mirror that jagged landscape: spaces mixed with underscores, erratic capitalizations, accented characters, and mismatched file extensions.

**Rime encases uneven filesystems in clean conventions:**

- **Surface Regularization**: Scans directories to sanitize erratic whitespace, special punctuation, and mixed casing into consistent, predictable naming conventions.
- **Deterministic Transformations**: Supports eight distinct casing formats, Unicode NFKD diacritic normalization, dry-run simulations, and transaction-logged rollback.

---

## Features

- **8 Case Transformation Modes**:
  - `Title_Snake_Case` (Default)
  - `standard_snake_case`
  - `UPPER_SNAKE_CASE`
  - `standard-kebab-case`
  - `PascalCase`
  - `camelCase`
  - `lowercase` / `UPPERCASE`
- **Word Boundary Tokenizer**: Splits camelCase, PascalCase, numbers, dots, hyphens, and underscores into cleanly parsed words prior to case transformation.
- **Safe ASCII Normalization**: Uses Unicode NFKD decomposition (`Café` $\to$ `Cafe`, `München` $\to$ `Munchen`) rather than destructively erasing international characters.
- **Atomic Undo Engine**: Records all operations in an undo journal for immediate rollback via `rime undo`.
- **Bottom-Up Directory Traversal**: In recursive directory mode, processes nested children before parents to maintain path validity.
- **Collision Protection**: Evaluates destination paths before renaming with configurable collision policies (`skip`, `suffix`, `abort`).
- **Dry-Run Previews**: Simulates planned renames with colored terminal diffs or structured JSON.
- **Model Context Protocol (MCP)**: Native stdio MCP server for agentic filesystem integrations.
- **Zero Host Dependencies**: Standard library core with sub-20ms execution time.

---

## Quick Start

Run Rime directly via Nix without installing:

```bash
# Sanitize files in the current directory to Title_Snake_Case (Default)
nix run github:SpanishSyntax/Rime

# Convert all filenames to standard_snake_case
nix run github:SpanishSyntax/Rime -- --snake

# Convert to standard-kebab-case with lowercase extensions
nix run github:SpanishSyntax/Rime -- --kebab --lower-ext

# Filter by extension (e.g. only PDF files)
nix run github:SpanishSyntax/Rime -- -e pdf --title-snake

# Safe ASCII mode with recursive directory traversal
nix run github:SpanishSyntax/Rime -- -r -s

# Dry-run preview
nix run github:SpanishSyntax/Rime -- --snake --dry-run

# Revert the last executed batch rename
nix run github:SpanishSyntax/Rime -- undo
```

---

## CLI Reference

```text
Usage: rime [paths...] [options]
       rime undo [options]
       rime mcp

Options:
  -d, --dir PATH         Target directory (Default: current directory)
  -e, --ext EXT          Filter by file extension (e.g., pdf, mp3, txt)
  -a, --all              Include hidden dotfiles (hard-excludes .git)
  -s, --safe             Safe ASCII: strip non-alphanumeric chars & normalize accents
  -l, --lower-ext        Convert file extensions to lowercase (Default: true)
  -r, --recursive        Recursively process subdirectories
  --dirs                 Also rename directory names
  --conflict MODE        Collision strategy: skip, suffix, abort (Default: skip)
  -n, --dry-run          Simulate changes without renaming any files
  -i, --interactive      Prompt for confirmation before applying renames
  -y, --yes              Bypass confirmation prompt
  -A, --agent            Compact machine-friendly output
  --json                 Structured JSON output
  --color MODE           Color output mode: auto, always, never (Default: auto)
  --no-color             Disable colored output
  -h, --help             Show help menu
  -V, -v, --version      Show version information

Case Transformations:
  --title-snake          Title_Snake_Case (Default)
  --snake                standard_snake_case
  --upper-snake          UPPER_SNAKE_CASE
  --kebab                standard-kebab-case
  --pascal               PascalCase
  --camel                camelCase
  --lower                lowercase
  --upper                UPPERCASE

Undo Options:
  -n, --dry-run          Preview operations that would be reverted
  -l, --list             List all recorded operations in undo history
```

---

## Configuration

Rime optionally loads defaults from `~/.config/rime/rime.toml`:

```toml
[general]
case_mode = "title_snake"
lower_ext = true
safe = false
on_conflict = "skip"
color = "auto"
```

---

## Home Manager Configuration

Add Rime to your `flake.nix`:

```nix
{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    rime = {
      url = "github:SpanishSyntax/Rime";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, rime, ... }: {
    homeConfigurations.user = home-manager.lib.homeManagerConfiguration {
      modules = [
        rime.homeManagerModules.default
        {
          programs.rime.enable = true;
        }
      ];
    };
  };
}
```

---

## License

MIT © SpanishSyntax
