import tkinter as tk
from tkinter import messagebox as ms
from tkinter import ttk

O: list[str] = [
    "KOPIEN ({})",
    "QUELLDATEIEN",
    "ZIELDATEIEN",
    "Fehlende Dateien",
    "Einige Dateien fehlen.",
]


class OperationFrame(ttk.Frame):
    def __init__(self, container: tk.Misc) -> None:
        super().__init__(container)

        self.count_var = tk.StringVar(value=O[0].format(0))

        ttk.Label(self, textvariable=self.count_var).grid(row=0, column=0, sticky="w", pady=(0, 4))

        self.tree = ttk.Treeview(self, columns=("source", "destination"), show="headings", selectmode="browse")
        self.tree.heading("source", text=O[1])
        self.tree.heading("destination", text=O[2])
        self.tree.column("source", width=400, minwidth=150, stretch=True)
        self.tree.column("destination", width=400, minwidth=150, stretch=True)
        self.tree.tag_configure("missing", foreground="#b00020", background="#ffd5dd")
        self.tree.tag_configure("warning", foreground="#a4b000", background="#fffcd5")
        self.tree.tag_configure("complete", foreground="#00b020", background="#deffd5")

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=1, column=0, sticky="nsew")
        vsb.grid(row=1, column=1, sticky="ns")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def set_operations(self, operations, problems: list[str], prefix: str = "") -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        are_problems: bool = len(problems) > 0
        showed_missing: bool = False

        for index, (source, destination) in enumerate(operations, start=1):
            if not are_problems:
                missing = not source.exists()

                if missing and not showed_missing:
                    ms.showwarning(O[3], O[4])
                    showed_missing = True

            src_text = str(source)
            dst_text = str(destination)

            if prefix:
                src_text = src_text[len(prefix):]
                dst_text = dst_text[len(prefix):]

            tags = ()

            if are_problems:
                # Very quirky and not elegant
                for p in problems:
                    if source.name in p:
                        tags = ("warning",)
            elif missing:
                tags = ("missing",)

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(src_text, dst_text),
                tags=tags,
            )

        self.count_var.set(O[0].format(len(operations)))
