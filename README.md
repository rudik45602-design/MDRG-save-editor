# MDRG Save Editor

A simple graphical save file editor for **My Dystopian Robot Girlfriend** (free version and beyond).

Allows you to edit in-game parameters — money, stats, relationship values, flags — directly from a `.mdrg` save file, without touching any game internals.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)

---

## Features

- 💰 Edit money and all numeric/string save parameters
- 🔎 Filter fields by name for quick navigation
- 📁 Handles both manual saves and auto-saves
- 🔄 Reset any field to its original value with one click
- 💾 Save in-place or export to a new file
- 🪟 No dependencies beyond the Python standard library

---

## Screenshots

> _Open your save file → edit values → save. That's it._

The editor shows all editable fields found in the save file. `money` is highlighted at the top.

---

## Requirements

- Python **3.8** or newer
- `tkinter` (included with most Python distributions)

---

## Installation

No installation needed. Just download the script and run it.

### Option 1 — Download the script directly

```bash
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/mdrg-save-editor/main/mdrg_editor.py
python mdrg_editor.py
```

### Option 2 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/mdrg-save-editor.git
cd mdrg-save-editor
python mdrg_editor.py
```

### On Linux — tkinter may need to be installed separately

```bash
# Debian / Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

---

## Usage

### With a GUI file picker

```bash
python mdrg_editor.py
```

Click **Open**, navigate to your save file, edit values, click **Save**.

### With a file argument (opens directly)

```bash
python mdrg_editor.py path/to/save.mdrg
```

---

## Where is my save file?

| OS | Path |
|---|---|
| **Windows** | `C:\Users\USERNAME\AppData\LocalLow\YotaGames\MyDystopianRobotGirlfriend\` |
| **Linux (Steam/Proton)** | `~/.steam/steam/steamapps/compatdata/<game_id>/pfx/drive_c/users/steamuser/AppData/LocalLow/YotaGames/MyDystopianRobotGirlfriend/` |
| **macOS** | `~/Library/Application Support/YotaGames/MyDystopianRobotGirlfriend/` |

On Windows, you can open the folder quickly by pressing **Win+R** and typing `%appdata%`, then navigating one level up to `AppData\LocalLow`.

> **Tip:** Make a backup copy of your `save.mdrg` before editing!

---

## Editable fields

The editor automatically discovers all editable fields in your save. Common ones include:

| Field | Description |
|---|---|
| `money` | In-game currency |
| `casinoTokens` | Casino token balance |
| `playerName` | Your character's name |
| `botName` | The robot girlfriend's name |
| `_health` | Health stat |
| `_stamina` | Stamina stat |
| `_satiation` | Hunger bar |
| `_mentalHealth` | Mental health stat |
| `_lust` | Relationship lust value |
| `_sympathy` | Relationship sympathy value |
| `_mood` | Bot mood |
| `subs` / `followers` | Streaming subscriber counts |
| `weeklyRent` | Weekly rent amount |
| ...and more | All numeric/string fields are shown |

> **Note:** If you open a very early-game save (just started), `savedata` may be empty and no fields will appear. Play a little further, save in-game, then open the file again.

---

## Why does my save show "no fields found"?

The game only writes detailed stats to `savedata` after the player progresses past the early prologue. If you just started, play until you get your first opportunity to save manually, then try the editor again.

---

## Limitations

- Does not edit game **flags** (story progression, events seen). Use the original [MDRG-save-editor](https://github.com/ORIGINAL_EDITOR_LINK) for that — it has a dedicated flags tab.
- Cannot decode the `storyTextIds_Comp` field (compressed story state).
- Editing some fields to extreme values may cause unexpected in-game behaviour.

---

## Contributing

Bug reports, suggestions, and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

---

## License

MIT — see [LICENSE](LICENSE) for details.
