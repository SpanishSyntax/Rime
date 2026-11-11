# Architecture & Design Philosophy

[Overview](README.md) • [Getting Started](getting-started.md) • [Architecture](architecture.md) • [CLI Reference](usage.md) • [Configuration](configuration.md)

---

## Design Philosophy

Rime adheres to strict systems engineering invariants:

1. **Non-Destructive by Default**: Never erase information silently. Unicode diacritics are decomposed rather than stripped; filename collisions are skipped by default rather than overwritten.
2. **Deterministic Tokenization**: Casing boundaries (e.g. `camelCase` $\to$ `camel` + `case`, `kebab-case` $\to$ `kebab` + `case`) are resolved via regularized lexical tokenization.
3. **Atomic Reversibility**: Every destructive filesystem batch operation is serialized to a transaction journal before execution, making rollback a single-step operation.

---

## The Lore

> **rime** (`/raɪm/`) — *noun:* A crystalline crust of ice formed when supercooled fog droplets freeze instantly upon contacting exposed surfaces, encasing irregular shapes in smooth, uniform white shells.

In subzero coastal air, jagged rocks, rough wire fences, and weather-beaten timber are steadily coated in rime—smoothed out and regularized into clean, unified crystalline forms. 

Project directories frequently mirror that jagged landscape: spaces mixed with underscores, erratic capitalizations, accented characters, and mismatched file extensions. Rime encases uneven filesystems in clean conventions through predictable, non-destructive tokenization.

---

## Word Boundary Detection

Naïve renaming scripts fail on strings that mix capitalization styles (e.g., `parseXMLDocument_v2.tar.gz`). Rime resolves filenames through a multi-pass regex tokenizer:

1. **Underscore & Hyphen Splitting**: Separates explicit delimiter boundaries (`foo_bar-baz`).
2. **CamelCase & PascalCase Splitting**: Detects lowercase-to-uppercase transitions (`getHTTPResponse` $\to$ `get`, `HTTP`, `Response`).
3. **Number Boundary Isolation**: Distinguishes numeric sequences attached to letters (`modelV2` $\to$ `model`, `V2`).
4. **Token Assembly**: Emits clean word tokens ready for target case formatting.

```
"myTest_file-v1.0.tar.gz"
       │
       ▼ (Boundary Splitting)
["my", "Test", "file", "v1", "0"] + [".tar.gz"]
       │
       ▼ (Case Transformation: e.g. --snake)
"my_test_file_v1_0.tar.gz"
```

---

## Unicode Accent Normalization

When `--safe` (`-s`) is active, Rime decomposes Unicode characters using **NFKD (Compatibility Decomposition)**:

- `é` decomposes into `e` + `\u0301` (combining acute accent).
- Non-spacing mark codepoints (category `Mn`) are stripped.
- The base ASCII glyph `e` is preserved intact.

This prevents destructive truncation (e.g. converting `Café.pdf` to `Caf.pdf` or `Caf_.pdf`), transforming it cleanly to `Cafe.pdf`.

---

## Bottom-Up Traversal

When renaming directory hierarchies recursively (`-r --dirs`), renaming a parent directory before its children invalidates all child file paths in the traversal stack.

Rime prevents path invalidation by:
1. Scanning the target directory tree and collecting all candidate files and directories.
2. Sorting items in **bottom-up order** (descending depth-first traversal).
3. Renaming leaf files first, then nested subdirectories, and finally parent directories.

---

## Collision and Transaction Safety

### Collision Strategies

If a destination path already exists on disk, Rime avoids unintentional overwriting according to `--conflict`:

- **`skip`** *(default)*: Skips the conflicting rename, outputs a clear warning, and proceeds with the rest of the batch.
- **`suffix`**: Automatically appends an incrementing numeric counter (`_1`, `_2`) before the extension.
- **`abort`**: Immediately terminates the entire operation before applying any file renames.

### Transaction Journal (`undo.json`)

Before executing renames, Rime writes the complete plan to an undo log located at `~/.cache/rime/undo.json` (or `$XDG_CACHE_HOME/rime/undo.json`):

```json
{
  "timestamp": "2026-11-11T01:15:30Z",
  "root": "/path/to/project",
  "operations": [
    {
      "original": "/path/to/project/Annual Report.pdf",
      "renamed": "/path/to/project/Annual_Report.pdf",
      "is_dir": false
    }
  ]
}
```

Running `rime undo` parses this journal in reverse order, verifying each file before moving it back to its original path.
