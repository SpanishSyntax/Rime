# Rime ❄️

> **Universal Filename Sanitizer, Case Transformer & Batch Rename Engine**

Rime is an ultra-fast, opinionated batch renaming utility designed to normalize messy filenames, standardize project conventions, and perform robust case transformations across large directories.

---

## ✨ Features

- 🔠 **8 Case Transformation Modes**:
  - `Title_Snake_Case` (Default)
  - `standard_snake_case`
  - `UPPER_SNAKE_CASE`
  - `standard-kebab-case`
  - `PascalCase`
  - `camelCase`
  - `lowercase` / `UPPERCASE`
- 🧠 **Smart Boundary Detection**: Automatically splits `camelCase`, `PascalCase`, dots, hyphens, and underscores into distinct words before transforming.
- 🌐 **Safe ASCII & Accent Normalization (`-s / --safe`)**: Decomposes Unicode diacritics (`Café` $\to$ `Cafe`, `München` $\to$ `Munchen`) rather than destructively erasing international characters.
- 🔄 **1-Command Undo Engine (`rime undo`)**: Stores a transaction journal in cache, allowing instant rollback of any batch rename operation.
- 🌲 **Recursive Traversal (`-r / --recursive`)**: Recursively processes subdirectories bottom-up so child files are renamed cleanly before parent directories.
- 📁 **Directory Renaming (`--dirs`)**: Option to sanitize and rename directory names alongside regular files.
- 🛡️ **Collision Protection**: Pre-checks target paths and prevents accidental overwrites if a file with the destination name already exists.
- 🧪 **Dry-Run Simulation (`-n / --dry-run`)**: Preview all planned changes in a colored diff view without touching the filesystem.
- 🪶 **Zero Host Dependencies**: Pure standard library core (<20ms execution time).

---

## 🚀 Quick Start

Run Rime directly via Nix without installing:

```bash
# Sanitize all files in the current directory to Title_Snake_Case (Default)
nix run github:SpanishSyntax/Rime

# Convert all filenames to standard_snake_case
nix run github:SpanishSyntax/Rime -- --snake

# Convert to standard-kebab-case with lowercase extensions
nix run github:SpanishSyntax/Rime -- --kebab --lower-ext

# Filter by extension (e.g. only audio or documentation files)
nix run github:SpanishSyntax/Rime -- -e pdf --title-snake

# Safe ASCII mode with recursive directory traversal
nix run github:SpanishSyntax/Rime -- -r -s

# Dry-run preview
nix run github:SpanishSyntax/Rime -- --snake --dry-run

# Revert the last executed batch rename
nix run github:SpanishSyntax/Rime -- undo
```

---

## 💻 CLI Commands & Options

```text
Usage: rime [paths...] [options]
       rime undo [options]

Options:
  -d, --dir PATH         Target directory (Default: current directory)
  -e, --ext EXT          Filter by file extension (e.g., pdf, mp3, txt)
  -a, --all              Include hidden dotfiles (hard-excludes .git)
  -s, --safe             Safe ASCII: strip non-alphanumeric chars & normalize accents
  -l, --lower-ext        Convert file extensions to lowercase
  -r, --recursive        Recursively process subdirectories
  --dirs                 Also rename directory names
  --on-conflict MODE     Collision strategy: skip, abort, suffix (Default: skip)
  -n, --dry-run          Simulate changes without renaming any files
  -i, --interactive      Prompt for confirmation before applying renames
  -y, --yes              Bypass confirmation prompt
  --color MODE           Color output mode: auto, always, never (Default: auto)
  --no-color             Disable colored output
  -h, --help             Show this help menu
  -V, -v, --version      Show version information

Undo Options:
  -n, --dry-run          Preview operations that would be reverted without modifying files
  -l, --list             List all recorded operations in undo history

Case Transformations:
  --title-snake          Title_Snake_Case (Default)
  --snake                standard_snake_case
  --upper-snake          UPPER_SNAKE_CASE
  --kebab                standard-kebab-case
  --pascal               PascalCase
  --camel                camelCase
  --lower                lowercase
  --upper                UPPERCASE
```

---

## 🛠️ Home Manager Configuration

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

Once enabled, `rime` is available in your `$PATH`.

---

## 📜 License

MIT © SpanishSyntax
