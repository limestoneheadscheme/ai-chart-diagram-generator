# Security Policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 0.6.x   | :white_check_mark: |
| 0.5.x   | :white_check_mark: |
| < 0.5   | :x:                |

## Reporting a vulnerability

This is a local-first desktop tool. It does not phone home, does not
run a relay, and does not execute LLM output as code. If you find a
way to make it do any of those three things, that is a security bug
and we want to hear about it.

Email: `security@ai-chart-diagram-generator.dev` (PGP key in
`docs/architecture/security.md`). Please include:

- A minimal reproducer (prompt + config + diagram type).
- The exact commit hash.
- Whether the issue is reachable from the default config.

We acknowledge within 72 hours and aim to ship a patch within 14 days
for high-severity issues.

## Scope

In scope:

- Sandbox escapes from the renderer adapter subprocesses (C++/C#/Java
  bridges).
- Prompt-injection paths that reach the file system or the shell.
- Deserialization of untrusted `.chartpack` files.
- Path traversal in the export service (`services/exporter.py`).

Out of scope:

- Denial of service from pathological prompts against a local model.
- Anything requiring the user to run with an already-compromised
  local LLM.
- Model quality / hallucinated diagrams. That's a prompt problem, not
  a security problem.

## Hardening notes for contributors

- Never `eval()` model output. The IR is parsed by the grammar
  modules; anything that doesn't parse is rejected, not executed.
- The C++ renderer shim runs in a subprocess with a 2-second wall
  clock and no network namespace on Linux; on Windows it runs with
  a job object limiting memory to 512 MB.
- All file writes go through `utils/fs.py::safe_write`, which refuses
  paths outside the configured export root.