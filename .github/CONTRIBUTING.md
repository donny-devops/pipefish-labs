# Contributing to PipeFish Labs

Welcome — and thank you for your interest in contributing to **PipeFish Labs**! 🐟
Whether you're reporting a bug, proposing a feature, improving documentation, or
submitting code, every contribution matters and is deeply appreciated.

Please take a moment to review these guidelines so we can keep the process smooth and
productive for everyone involved.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to File Issues](#how-to-file-issues)
  - [Bug Reports](#bug-reports)
  - [Feature Requests](#feature-requests)
- [Pull Request Guidelines](#pull-request-guidelines)
  - [Branch Naming](#branch-naming)
  - [Commit Message Conventions](#commit-message-conventions)
  - [Pull Request Template](#pull-request-template)
- [Code Style Expectations](#code-style-expectations)
- [Security Vulnerability Reporting](#security-vulnerability-reporting)
- [Development Setup](#development-setup)

---

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you
are expected to uphold this code. Please read the full text at
[CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) before contributing.

---

## How to File Issues

### Bug Reports

If you encounter a bug, please open a
[GitHub Issue](https://github.com/pipefish-labs/pipefish-labs/issues/new) with the
following information:

- **Summary** — A clear, concise description of the problem.
- **Steps to Reproduce** — Numbered steps to reliably trigger the bug.
- **Expected Behavior** — What you expected to happen.
- **Actual Behavior** — What actually happened.
- **Environment** — OS, browser/version, Python version, and any relevant dependency
  versions.
- **Screenshots / Logs** — Attach console output, stack traces, or screenshots if
  applicable.

### Feature Requests

We love hearing new ideas! When proposing a feature:

- **Describe the problem** the feature solves or the opportunity it creates.
- **Propose a solution** with as much detail as you can provide (API design, UI mockups,
  architecture diagrams, etc.).
- **Consider alternatives** — Have you explored other approaches? Let us know why this
  one is preferred.
- **Label your issue** with `enhancement`.

---

## Pull Request Guidelines

### Branch Naming

Use the following conventions for branch names:

| Type        | Pattern                           | Example                          |
| ----------- | --------------------------------- | -------------------------------- |
| Feature     | `feature/<short-description>`     | `feature/add-webhook-retry`      |
| Bug fix     | `fix/<short-description>`         | `fix/graph-timeout-handling`     |
| Docs        | `docs/<short-description>`        | `docs/update-api-reference`      |
| Refactor    | `refactor/<short-description>`    | `refactor/agent-orchestration`   |
| Chore/CI    | `chore/<short-description>`       | `chore/upgrade-lighthouse-ci`    |

### Commit Message Conventions

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`,
`chore`, `revert`

**Examples:**

```
feat(agents): add native Mistral handoff support
fix(sdk): correct bearer token refresh logic
docs(readme): update development setup instructions
ci(lighthouse): add performance assertion thresholds
```

- Use the **imperative mood** in the subject line ("add", not "added").
- Keep the subject line to **72 characters or fewer**.
- Reference related issues in the footer: `Closes #42`.

### Pull Request Template

When opening a PR, please include:

1. **Description** — What does this PR do and why?
2. **Related Issues** — Link to any related GitHub Issues (e.g., `Closes #123`).
3. **Type of Change** — Bug fix, feature, docs, refactor, etc.
4. **Testing** — Describe how you tested your changes.
5. **Checklist:**
   - [ ] My code follows the project's code style guidelines.
   - [ ] I have performed a self-review of my code.
   - [ ] I have added/updated tests where applicable.
   - [ ] I have updated documentation where applicable.
   - [ ] All new and existing tests pass locally.

---

## Code Style Expectations

### Python

- Follow **[PEP 8](https://peps.python.org/pep-0008/)** for all Python code.
- Use type hints wherever possible.
- Lint your code with `flake8` or `ruff` before submitting.
- Format with `black` (line length: 88).
- Write docstrings using the
  [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

### HTML

- Use **semantic markup** (`<header>`, `<nav>`, `<main>`, `<section>`, `<article>`,
  `<footer>`, etc.) instead of generic `<div>` elements.
- Follow accessibility best practices (ARIA attributes, alt text, landmark roles).
- Maintain clean indentation (2 spaces).

### General

- Remove trailing whitespace.
- End files with a single newline.
- Keep functions focused and single-purpose.

---

## Security Vulnerability Reporting

> **⚠️ Do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, please follow the responsible disclosure
process described in our [SECURITY.md](SECURITY.md). In short:

1. Open a **Private Vulnerability Report** through the
   [GitHub Security Advisory](https://github.com/pipefish-labs/pipefish-labs/security/advisories)
   tab.
2. You will receive an initial acknowledgment within **48 hours**.
3. We will coordinate a timeline for mitigation and public disclosure.

---

## Development Setup

### Prerequisites

- **Python 3.11+** (3.12 is fine; CI uses 3.11)
- **Git**
- **Node.js 22+** only if you need `make preview` / `make deploy` (Wrangler via `npx`; no global install)

Prefer `python3 -m …` and `make` targets over bare `pytest` / `pipefish` binaries. A `--user` pip install puts scripts in `~/.local/bin`, which is often not on `PATH`.

### Getting Started

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/<your-username>/pipefish-labs.git
   cd pipefish-labs
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   .venv\Scripts\activate      # Windows
   ```

3. **Install the package and dev extras** (same command as CI; there is no `requirements.txt`):

   ```bash
   python3 -m pip install -e ".[dev]"
   ```

4. **Run the checks required before a PR:**

   ```bash
   make test
   make verify-dom
   ```

   `make test` runs `python -m unittest discover -s tests -p "test_*.py"`.
   `make verify-dom` validates landing-page DOM and media integrity.

5. **Preview the site:**

   ```bash
   make serve
   ```

   This builds `dist/` and serves it on `http://127.0.0.1:8787` with the stdlib HTTP server. It does not need Wrangler, npm credentials, or a Cloudflare account.

   For production-parity edge routing, `_headers`, and `_redirects`:

   ```bash
   make preview
   ```

   That runs `npx wrangler dev` (Wrangler is downloaded on first use; do not `npm install -g wrangler`).

6. **Create a feature branch and start coding:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

### Cloud Agents

[`.cursor/environment.json`](../.cursor/environment.json) is the repo-managed Cloud Agent environment. `install` runs the same editable install as CI and builds `dist/`. `start` runs `python3 scripts/serve_preview.py`, which is idempotent: it reuses a listener already bound on port 8787, or detaches a new one and returns once `GET /` succeeds.

---

## Thank You!

Every contribution — large or small — helps make PipeFish Labs better for the entire
community. We look forward to collaborating with you! 🚀
