#!/usr/bin/env python3
"""
MDRG Save Editor — редактор сохранений My Dystopian Robot Girlfriend
Поддерживает редактирование всех найденных числовых и строковых полей,
включая вложенный savedata.
"""

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import sys

# Читаемые названия для известных полей
FIELD_LABELS = {
    "money": "💰 Деньги (money)",
    "casinoTokens": "🎰 Жетоны казино",
    "playerName": "👤 Имя игрока",
    "botName": "🤖 Имя бота",
    "_stamina": "⚡ Выносливость",
    "_satiation": "🍔 Сытость",
    "_health": "❤️ Здоровье",
    "_mentalHealth": "🧠 Психическое здоровье",
    "_mentalHealthTemporary": "🧠 Психическое здоровье (врем.)",
    "_lust": "💜 Влечение",
    "_longing": "💙 Тоска",
    "_currentHorniness": "💛 Возбуждение",
    "_sympathy": "💚 Симпатия",
    "_mood": "😊 Настроение",
    "inteligence": "🎓 Интеллект",
    "weeklyRent": "🏠 Аренда в неделю",
    "subs": "📺 Подписчики",
    "followers": "📱 Фолловеры",
    "nunPoints": "⛪ Очки монашки",
    "priestBotPoints": "✝️ Очки священника-бота",
    "gameVersion": "🎮 Версия игры",
    "search": "🔍 Поиск",
    "ingameTime": "⏱ Игровое время (мин)",
    "lastWorkedAtDay": "💼 Последний рабочий день",
    "timesWentToChurch": "⛪ Посещений церкви",
}

# Поля, которые лучше не показывать (служебные/неинтересные)
SKIP_FIELDS = {
    "storyTextIds_Comp", "visitedWebsites", "achievements", "flags",
    "saves", "autoSaves", "nextAutoSaveIndex", "savedata",
    "_time", "slot", "_saveType", "notes", "description",
}


def flatten_savedata(save: dict) -> dict:
    """Достаёт данные из вложенного savedata JSON."""
    result = {}
    savedata_raw = save.get("savedata", "")
    if savedata_raw and savedata_raw != "{}":
        try:
            inner = json.loads(savedata_raw) if isinstance(savedata_raw, str) else savedata_raw
            result.update(inner)
        except (json.JSONDecodeError, TypeError):
            pass
    return result


def get_all_editable(data: dict) -> dict:
    """Собирает все редактируемые поля из корня и из savedata слотов."""
    fields = {}

    # Поля верхнего уровня (не вложенные, не служебные)
    for k, v in data.items():
        if k in SKIP_FIELDS:
            continue
        if isinstance(v, (str, int, float, bool)) and not isinstance(v, bool):
            fields[("root", k)] = v

    # Поля из каждого слота saves/autoSaves
    for slot_type in ("saves", "autoSaves"):
        for save in data.get(slot_type, []):
            slot_id = save.get("slot", "?")
            inner = flatten_savedata(save)
            for k, v in inner.items():
                if isinstance(v, (str, int, float)) and not isinstance(v, bool):
                    fields[(f"{slot_type}[{slot_id}]", k)] = v

    return fields


class SaveEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MDRG Save Editor")
        self.geometry("750x600")
        self.resizable(True, True)

        self.file_path = None
        self.raw_data = None
        self.vars = {}  # (source, key) -> tk.Variable

        self._build_ui()

        # Если файл передан аргументом командной строки
        if len(sys.argv) > 1:
            path = Path(sys.argv[1])
            if path.exists():
                self._load_file(path)

    def _build_ui(self):
        # ── Верхняя панель ──
        top = tk.Frame(self, pady=4)
        top.pack(fill=tk.X, padx=8)

        tk.Button(top, text="📂 Открыть .mdrg", command=self._open_file, width=18).pack(side=tk.LEFT)
        tk.Button(top, text="💾 Сохранить", command=self._save_file, width=14).pack(side=tk.LEFT, padx=4)
        tk.Button(top, text="💾 Сохранить как...", command=self._save_as_file, width=18).pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Откройте файл сохранения (.mdrg)")
        tk.Label(top, textvariable=self.status_var, fg="gray").pack(side=tk.LEFT, padx=8)

        # ── Поиск ──
        search_frame = tk.Frame(self, pady=2)
        search_frame.pack(fill=tk.X, padx=8)
        tk.Label(search_frame, text="🔎 Фильтр:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._filter_rows())
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=4)
        tk.Button(search_frame, text="✕", command=lambda: self.search_var.set(""), width=2).pack(side=tk.LEFT)

        # ── Таблица с прокруткой ──
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        self.canvas = tk.Canvas(container, borderwidth=0, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.rows_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")

        self.rows_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)

        # Все строки виджетов для фильтрации
        self.all_rows = []  # list of (frame, source, key, label)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        else:
            self.canvas.yview_scroll(1, "units")

    def _open_file(self):
        path = filedialog.askopenfilename(
            title="Открыть файл сохранения",
            filetypes=[("MDRG save files", "*.mdrg"), ("All files", "*.*")]
        )
        if path:
            self._load_file(Path(path))

    def _load_file(self, path: Path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.raw_data = json.load(f)
            self.file_path = path
            self.status_var.set(f"✅ {path.name}")
            self._populate_fields()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")
            self.status_var.set("❌ Ошибка открытия файла")

    def _populate_fields(self):
        # Очистить старые виджеты
        for widget in self.rows_frame.winfo_children():
            widget.destroy()
        self.vars.clear()
        self.all_rows.clear()

        fields = get_all_editable(self.raw_data)

        if not fields:
            tk.Label(
                self.rows_frame,
                text="⚠️ Поля для редактирования не найдены.\n"
                     "Возможно, savedata пуст — начните игру и сохранитесь хотя бы раз.",
                justify=tk.LEFT, fg="orange", pady=20
            ).pack(padx=10)
            return

        # Заголовок таблицы
        header = tk.Frame(self.rows_frame, bg="#dde")
        header.pack(fill=tk.X, pady=(0, 2))
        tk.Label(header, text="Источник", width=18, anchor="w", bg="#dde", font=("", 9, "bold")).pack(side=tk.LEFT, padx=4)
        tk.Label(header, text="Параметр", width=30, anchor="w", bg="#dde", font=("", 9, "bold")).pack(side=tk.LEFT, padx=4)
        tk.Label(header, text="Значение", width=20, anchor="w", bg="#dde", font=("", 9, "bold")).pack(side=tk.LEFT, padx=4)

        # Сортируем: сначала деньги, потом известные поля, потом остальные
        def sort_key(item):
            (src, key), val = item
            if key == "money":
                return (0, key)
            if key in FIELD_LABELS:
                return (1, key)
            return (2, key)

        sorted_fields = sorted(fields.items(), key=sort_key)

        for (source, key), value in sorted_fields:
            label_text = FIELD_LABELS.get(key, key)
            row = self._make_row(source, key, label_text, value)
            self.all_rows.append((row, source, key, label_text))

    def _make_row(self, source: str, key: str, label_text: str, value) -> tk.Frame:
        bg = "#fff8e1" if key == "money" else ("white" if len(self.all_rows) % 2 == 0 else "#f5f5f5")

        row = tk.Frame(self.rows_frame, bg=bg, pady=2)
        row.pack(fill=tk.X)

        # Источник (saves[0], root, ...)
        src_label = "Основной файл" if source == "root" else source
        tk.Label(row, text=src_label, width=18, anchor="w", bg=bg, fg="gray", font=("", 8)).pack(side=tk.LEFT, padx=4)

        # Название поля
        tk.Label(row, text=label_text, width=30, anchor="w", bg=bg).pack(side=tk.LEFT, padx=4)

        # Поле ввода
        if isinstance(value, float):
            var = tk.DoubleVar(value=value)
        elif isinstance(value, int):
            var = tk.IntVar(value=value)
        else:
            var = tk.StringVar(value=str(value))

        self.vars[(source, key)] = var

        entry_frame = tk.Frame(row, bg=bg)
        entry_frame.pack(side=tk.LEFT)

        if isinstance(value, (int, float)) and key not in ("ingameTime", "lastWorkedAtDay",
                                                             "lastHungerInfoAt", "lastMentalHealthInfoAt",
                                                             "lastWokeUpAt", "lastWentToChurchAt"):
            entry = tk.Spinbox(
                entry_frame,
                textvariable=var,
                from_=0 if isinstance(value, int) else 0.0,
                to=9_999_999_999,
                increment=1,
                width=20,
                font=("Courier", 10, "bold") if key == "money" else ("", 10),
            )
        else:
            entry = tk.Entry(entry_frame, textvariable=var, width=22,
                             font=("Courier", 10, "bold") if key == "money" else ("", 10))
        entry.pack(side=tk.LEFT)

        # Кнопка сброса
        def reset(v=var, orig=value):
            if isinstance(orig, float):
                v.set(orig)
            elif isinstance(orig, int):
                v.set(orig)
            else:
                v.set(str(orig))

        tk.Button(row, text="↩", command=reset, width=2, bg=bg, relief=tk.FLAT,
                  cursor="hand2", fg="gray").pack(side=tk.LEFT, padx=2)

        return row

    def _filter_rows(self):
        query = self.search_var.get().lower()
        for row, source, key, label in self.all_rows:
            if not query or query in key.lower() or query in label.lower() or query in source.lower():
                row.pack(fill=tk.X)
            else:
                row.pack_forget()

    def _collect_changes(self) -> dict:
        """Собирает изменённые значения и возвращает обновлённый raw_data."""
        import copy
        data = copy.deepcopy(self.raw_data)

        # Группируем изменения по источнику
        root_changes = {}
        slot_changes = {}  # "saves[0]" -> {key: val}

        for (source, key), var in self.vars.items():
            try:
                val = var.get()
            except tk.TclError:
                continue

            if source == "root":
                root_changes[key] = val
            else:
                slot_changes.setdefault(source, {})[key] = val

        # Применяем root изменения
        data.update(root_changes)

        # Применяем изменения в savedata
        for slot_key, changes in slot_changes.items():
            # slot_key вида "saves[0]" или "autoSaves[2]"
            if "[" in slot_key:
                list_name, idx_str = slot_key.rstrip("]").split("[")
                slot_idx = int(idx_str)
                for save in data.get(list_name, []):
                    if save.get("slot") == slot_idx:
                        # Читаем savedata
                        sd_raw = save.get("savedata", "{}")
                        try:
                            sd = json.loads(sd_raw) if isinstance(sd_raw, str) else sd_raw
                        except (json.JSONDecodeError, TypeError):
                            sd = {}
                        sd.update(changes)
                        save["savedata"] = json.dumps(sd, ensure_ascii=False)
                        break

        return data

    def _save_file(self):
        if not self.file_path:
            self._save_as_file()
            return
        self._write_file(self.file_path)

    def _save_as_file(self):
        path = filedialog.asksaveasfilename(
            title="Сохранить как...",
            defaultextension=".mdrg",
            filetypes=[("MDRG save files", "*.mdrg"), ("All files", "*.*")],
            initialfile=self.file_path.name if self.file_path else "save_edited.mdrg"
        )
        if path:
            self._write_file(Path(path))

    def _write_file(self, path: Path):
        try:
            updated = self._collect_changes()
            with open(path, "w", encoding="utf-8") as f:
                json.dump(updated, f, ensure_ascii=False, indent=2)
            self.file_path = path
            self.status_var.set(f"✅ Сохранено: {path.name}")
            messagebox.showinfo("Готово", f"Файл сохранён:\n{path}")
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", str(e))
            self.status_var.set("❌ Ошибка сохранения")


if __name__ == "__main__":
    app = SaveEditor()
    app.mainloop()
