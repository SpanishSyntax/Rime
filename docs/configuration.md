# Configuration & Advanced Options

[Overview](README.md) • [Getting Started](getting-started.md) • [Architecture](architecture.md) • [CLI Reference](usage.md) • [Configuration](configuration.md)

---

## Configuration File

Rime reads optional default settings from `~/.config/rime/rime.toml` (or `$XDG_CONFIG_HOME/rime/rime.toml`).

### Specification (`rime.toml`)

```toml
[general]
# Default case mode to use when no CLI flag is provided
# Options: title_snake, snake, kebab, pascal, camel, lower, upper, upper_snake
case_mode = "title_snake"

# Default file extension filter ("*" for all files)
ext = "*"

# Whether to scan subdirectories recursively by default
recursive = false

# Whether to rename directories as well as files
include_dirs = false

# Whether to process hidden files (dotfiles)
include_hidden = false

# Strict ASCII normalization (decompose accents and remove special characters)
safe = false

# Enforce lowercase file extensions (.PDF -> .pdf)
lower_ext = true

# Conflict resolution strategy: skip, suffix, or abort
on_conflict = "skip"

# Terminal color mode: auto, always, or never
color = "auto"
```

Any options passed on the command line override values defined in `rime.toml`.

---

## NixOS and Home Manager

### NixOS System Module

```nix
# flake.nix or configuration.nix
{
  programs.rime = {
    enable = true;
    package = inputs.rime.packages.${pkgs.system}.default;
  };
}
```

### Home Manager Module

The Home Manager module allows declarative management of Rime and its configuration file:

```nix
{
  programs.rime = {
    enable = true;
    settings = {
      general = {
        case_mode = "snake";
        lower_ext = true;
        safe = true;
        on_conflict = "suffix";
      };
    };
  };
}
```

When enabled, Home Manager generates `~/.config/rime/rime.toml` using `pkgs.formats.toml`.
