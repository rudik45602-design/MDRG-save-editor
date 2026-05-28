# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2025-05-28

### Added
- Initial release of MDRG Save Editor
- Graphical interface built with Python's standard `tkinter` library — no external dependencies
- Automatic discovery of all editable numeric and string fields from `.mdrg` save files
- Support for both manual saves (`saves`) and auto-saves (`autoSaves`)
- Proper handling of nested `savedata` JSON within each save slot
- `money` field highlighted and sorted to the top for quick access
- Human-readable labels for known game fields (money, health, stamina, relationship stats, etc.)
- Live filter/search bar to quickly find fields by name
- Per-field reset button (`↩`) to revert to the original loaded value
- Save in-place or export to a new file via "Save As..."
- Command-line argument support: `python mdrg_editor.py save.mdrg` opens the file directly
- Clear warning when `savedata` is empty (early-game save with no stats yet written)
- Mouse wheel scrolling support on the fields list

---

## [Unreleased]

### Planned
- Flag editor tab (story progression / events seen)
- Dark mode
- Field validation with min/max hints per stat
- Drag-and-drop file opening
