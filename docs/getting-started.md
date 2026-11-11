# Getting Started with Rime

[Overview](README.md) • [Getting Started](getting-started.md) • [Architecture](architecture.md) • [CLI Reference](usage.md) • [Configuration](configuration.md)

---

## Installation

### Running Directly via Nix (Recommended)

Run Rime on any directory without global host installation:

```bash
# Run interactive wizard in current directory
nix run github:SpanishSyntax/Rime

# Convert all files to kebab-case
nix run github:SpanishSyntax/Rime -- --kebab
```

### Home Manager

Add Rime to your flake inputs and include its module:

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

### NixOS System Configuration

```nix
{
  programs.rime.enable = true;
  programs.rime.package = inputs.rime.packages.${pkgs.system}.default;
}
```

### Installing via Pip / Uv

```bash
# Using uv
uv tool install git+https://github.com/SpanishSyntax/Rime.git

# Using pip
pip install git+https://github.com/SpanishSyntax/Rime.git
```

---

## Quick Start

### 1. Default Title Snake Case

Format all files in the current folder using the default `Title_Snake_Case`:

```bash
rime
```

Rime displays a preview panel showing the planned renames, highlighted collisions (if any), and asks for confirmation before applying changes.

### 2. Standardizing a Code Repository to Snake Case

To standardize filenames across an entire repository without touching directory names:

```bash
rime --snake -r
```

### 3. Cleaning Documentation Files to Kebab Case

To standardize only Markdown and PDF files with safe ASCII diacritic replacement:

```bash
rime --kebab -e md -s -r
rime --kebab -e pdf -s -r
```

### 4. Simulating Changes Safely (Dry Run)

To preview planned renames without writing any changes to disk:

```bash
rime --snake --dry-run
```

### 5. Reverting Previous Renames

If a batch rename produced unintended results, rollback the entire batch immediately:

```bash
rime undo
```
