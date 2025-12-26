import os
import json
import logging
import tkinter as tk
from tkinter import ttk


class CalculationHistory:
    def __init__(self, master, history_file=None, max_entries: int = 20):
        self.log = logging.getLogger(__name__)

        self.master = master
        self.entries = []
        self.max_entries = max_entries
        if history_file:
            self.history_file = history_file
        else:
            self.history_file = os.path.join(os.path.dirname(__file__), "history.json")

        # load existing
        self._load()

        self.frame = tk.Frame(master, bg="#f7f7f7")
        self.frame.pack(fill="both", expand=True)

        top = tk.Frame(self.frame, bg="#f7f7f7")
        top.pack(fill="x", padx=8, pady=8)

        tk.Label(top, text="Calculation History", font=("Arial", 12, "bold"), bg="#f7f7f7").pack(side="left")
        btn_frame = tk.Frame(top, bg="#f7f7f7")
        btn_frame.pack(side="right")

        self.clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear, bg="#ff5e5e", fg="white", bd=0)
        self.clear_btn.pack(side="right", padx=(4, 0))

        self.copy_btn = tk.Button(btn_frame, text="Copy", command=self.copy_to_clipboard, bg="#2ecc71", fg="white", bd=0)
        self.copy_btn.pack(side="right", padx=(0, 4))

        list_frame = tk.Frame(self.frame, bg="#f7f7f7")
        list_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.scrollbar = tk.Scrollbar(list_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(list_frame, yscrollcommand=self.scrollbar.set, font=("Consolas", 11))
        self.listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.bind("<Double-1>", self._on_double_click)

        for e in self.entries:
            try:
                self.listbox.insert(tk.END, e)
            except Exception:
                pass

    def apply_theme(self, theme: dict):
        try:
            bg = theme.get("bg", "#f7f7f7")
            fg = theme.get("fg", "#232b36")
            entry_bg = theme.get("entry_bg", "#ffffff")
            self.frame.configure(bg=bg)
            for w in (self.listbox, self.scrollbar, self.clear_btn, self.copy_btn):
                try:
                    w.configure(bg=entry_bg, fg=fg)
                except Exception:
                    pass
        except Exception:
            pass

    def add_entry(self, text: str):
        entry = text.strip()
        if not entry:
            return
        self.entries.append(entry)
        if len(self.entries) > self.max_entries:
            try:
                self.entries.pop(0)
                self.listbox.delete(0)
            except Exception:
                pass
        try:
            self.listbox.insert(tk.END, entry)
            self.listbox.see(tk.END)
        except Exception:
            pass
        try:
            self._save()
            self.log.info(f"History added: {entry}")
        except Exception:
            pass

    def clear(self):
        self.entries.clear()
        self.listbox.delete(0, tk.END)
        try:
            self._save()
            self.log.info("History cleared")
        except Exception:
            pass

    def copy_to_clipboard(self):
        try:
            all_text = "\n".join(self.entries)
            self.master.clipboard_clear()
            self.master.clipboard_append(all_text)
        except Exception:
            pass

    def _on_double_click(self, event):
        try:
            idx = self.listbox.curselection()
            if not idx:
                return
            text = self.listbox.get(idx)
            self.master.clipboard_clear()
            self.master.clipboard_append(text)
        except Exception:
            pass

    def _save(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.entries, f, indent=2)
        except Exception:
            pass

    def _load(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.entries = data[-self.max_entries:]
                    else:
                        self.entries = []
        except Exception:
            self.entries = []

    def get_frame(self):
        return self.frame
