# Contributing

Thank you for considering a contribution to MDRG Save Editor!  
This is a small community tool, so contributions of any size are appreciated.

---

## Ways to contribute

- **Report a bug** — open an issue with steps to reproduce, your OS, and Python version
- **Suggest a feature** — open an issue describing what you'd like and why
- **Submit a fix or improvement** — open a pull request (see below)
- **Add missing field labels** — if you find an in-game field that isn't labelled yet, a one-line addition to `FIELD_LABELS` in the script is very welcome

---

## Development setup

The project has no external dependencies — just Python 3.8+ with `tkinter`.

```bash
git clone https://github.com/YOUR_USERNAME/mdrg-save-editor.git
cd mdrg-save-editor
python mdrg_editor.py
```

That's all there is to it. No virtual environment or `pip install` needed.

---

## Pull request guidelines

1. Fork the repository and create a branch from `main`.
2. Keep changes focused — one fix or feature per PR.
3. Test with at least one real `.mdrg` save file.
4. Update `CHANGELOG.md` under `[Unreleased]` with a brief description of your change.
5. Open the PR and describe what you changed and why.

---

## Code style

- Follow the existing style (PEP 8, 4-space indentation).
- Keep the zero-dependency constraint — do **not** add any `pip` packages.
- New field labels go in the `FIELD_LABELS` dict, alphabetically within their group.
- Keep comments in English so the codebase stays accessible to international contributors.

---

## Reporting save file issues

If the editor doesn't read your save correctly, please include:

- Your OS and Python version (`python --version`)
- Whether the save was from the free or paid version of the game
- A **sanitized** copy of your save file (you can replace string values like your name with placeholder text)

Do **not** post your full unmodified save file publicly if you're concerned about privacy.
