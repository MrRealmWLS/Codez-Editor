from turtle import back
from PIL import Image
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog
import os, re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BG = "#262624"
BG2 = "#30302e"
TEXT = "#f0f0f0"
MUTED = "#6f6e6a"
ACCENT = "#9d4edd"
HOVER = "#b57ae0"
SYNTAX = {
    "keyword":  ("#c678dd", r"\b(def|class|return|import|from|if|else|elif|for|while|in|not|and|or|True|False|None|try|except|with|as|pass|break|continue|lambda|yield|global|nonlocal|raise|del|assert)\b"),
    "builtin":  ("#61afef", r"\b(print|len|range|type|int|str|float|list|dict|set|tuple|open|super|self|cls|input|enumerate|zip|map|filter|hasattr|getattr|setattr)\b"),
    "string":   ("#98c379", r"(\"\"\"[\s\S]*?\"\"\"|\'\'\'[\s\S]*?\'\'\'|\"[^\"\\n]*\"|\'[^\'\\n]*\')"),
    "comment":  ("#5c6370", r"#[^\n]*"),
    "number":   ("#d19a66", r"\b\d+(\.\d+)?\b"),
    "decorator":("#e5c07b", r"@\w+"),
}

WORKSPACE = os.getcwd()

root = ctk.CTk()
root.title("Codez Editor")
root.geometry("1350x760")
root.configure(fg_color=BG)


def input_dialog(title, label, initial=""):
    win = ctk.CTkToplevel(root)
    win.title(title)
    win.geometry("360x160")
    win.configure(fg_color=BG2)
    win.grab_set()

    ctk.CTkLabel(win, text=label).pack(pady=(20, 8))
    entry = ctk.CTkEntry(win)
    entry.insert(0, initial)
    entry.pack(padx=20, fill="x")
    entry.focus()

    result = {"val": None}

    def submit():
        result["val"] = entry.get().strip()
        win.destroy()

    ctk.CTkButton(
        win, text="Confirm",
        fg_color=ACCENT, hover_color=HOVER,
        command=submit
    ).pack(pady=14)

    win.wait_window()
    return result["val"]

def confirm_dialog(title, message):
    win = ctk.CTkToplevel(root)
    win.title(title)
    win.geometry("360x160")
    win.configure(fg_color=BG2)
    win.grab_set()

    result = {"ok": False}

    ctk.CTkLabel(win, text=message, wraplength=300).pack(pady=20)

    def yes():
        result["ok"] = True
        win.destroy()

    frame = ctk.CTkFrame(win, fg_color="transparent")
    frame.pack()

    ctk.CTkButton(frame, text="Cancel", command=win.destroy).pack(side="left", padx=10)
    ctk.CTkButton(
        frame, text="Delete",
        fg_color=ACCENT, hover_color=HOVER,
        command=yes
    ).pack(side="left", padx=10)

    win.wait_window()
    return result["ok"]

header = ctk.CTkFrame(root, fg_color=BG2, height=40)
header.pack(fill="x")

ctk.CTkLabel(header, text="Codez Editor", font=("Segoe UI", 13, "bold")).pack(
    side="left", padx=14
)
status = ctk.CTkLabel(header, text="Ready", text_color=MUTED)
status.pack(side="right", padx=14)

toolbar = ctk.CTkFrame(root, fg_color=BG2)
toolbar.pack(fill="x")

def choose_workspace():
    global WORKSPACE
    path = filedialog.askdirectory()
    if path:
        WORKSPACE = path
        refresh_tree()

ctk.CTkButton(
    toolbar, text="Open Folder",
    fg_color=ACCENT, hover_color=HOVER,
    command=choose_workspace
).pack(side="left", padx=8, pady=6)

main = ctk.CTkFrame(root, fg_color=BG,bg_color=BG)
main.pack(fill="both", expand=True)

explorer = ctk.CTkFrame(main, width=260, fg_color=BG2)
explorer.pack(side="left", fill="y")

explorer_bar = ctk.CTkFrame(explorer, fg_color=BG2)
explorer_bar.pack(fill="x", padx=6, pady=6)

def new_file():
    name = input_dialog("New File", "File name:")
    if not name:
        return
    path = os.path.join(WORKSPACE, name)
    if os.path.exists(path):
        return
    open(path, "w", encoding="utf-8").close()
    refresh_tree()

def new_folder():
    name = input_dialog("New Folder", "Folder name:")
    if name:
        os.makedirs(os.path.join(WORKSPACE, name), exist_ok=True)
        refresh_tree()

def rename_item():
    sel = tree.selection()
    if not sel:
        return
    old = tree.item(sel[0], "values")[0]
    new = input_dialog("Rename", "New name:", os.path.basename(old))
    if new:
        new_path = os.path.join(os.path.dirname(old), new)
        os.rename(old, new_path)
        close_tab_by_path(old)
        refresh_tree()

def delete_item():
    sel = tree.selection()
    if not sel:
        return
    path = tree.item(sel[0], "values")[0]
    if confirm_dialog("Delete", f"Delete {os.path.basename(path)}?"):
        if os.path.isfile(path):
            os.remove(path)
        else:
            os.rmdir(path)
        close_tab_by_path(path)
        refresh_tree()

for txt, cmd in [("assests\\new-file.png", new_file), ("assests\\new-folder.png", new_folder),
                 ("assests\\rename.png", rename_item), ("assests\\trash.png", delete_item)]:
    img = Image.open(txt)
    ctk.CTkButton(
        explorer_bar,
        text="", 
        width=15,
        fg_color=ACCENT,
        hover_color=HOVER,
        command=cmd,
        image=ctk.CTkImage(light_image=img, size=(15, 15))
    ).pack(side="left", padx=2)
tree_frame = tk.Frame(explorer, background=BG2)
tree_frame.pack(fill="both", expand=True, padx=6, pady=6)
style = ttk.Style()
style.theme_use("alt")
style.configure("Treeview", background=BG2, fieldbackground=BG2, foreground=TEXT)
style.layout("Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

tree = ttk.Treeview(tree_frame, show="tree")

tree.pack(fill="both", expand=True)

def populate_tree(parent, path):
    try:
        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            node = tree.insert(parent, "end", text=name, values=[full])
            if os.path.isdir(full):
                populate_tree(node, full)
    except PermissionError:
        pass

def refresh_tree():
    tree.delete(*tree.get_children())
    populate_tree("", WORKSPACE)
notebook = ttk.Notebook(main)
style = ttk.Style()
style.theme_use("alt") 

style.layout("TNotebook", [("Notebook.client", {"sticky": "nswe"})])

style.configure("TNotebook",
                background=BG,
                borderwidth=0,
                tabmargins=[2,5,2,0])
style.configure("TNotebook.Tab",
                background="#444444",
                foreground=TEXT,
                padding=[10,5],
                borderwidth=0)

style.map("TNotebook.Tab",
          background=[("selected", BG)],
          foreground=[("selected", TEXT)])

notebook.pack(side="right", fill="both", expand=True)
tabs = {}
def highlight(t_widget):
    content = t_widget.get("1.0", "end")
    for tag in SYNTAX:
        t_widget.tag_remove(tag, "1.0", "end")

    for tag, (color, pattern) in SYNTAX.items():
        t_widget.tag_configure(tag, foreground=color)
        for match in re.finditer(pattern, content):
            start = f"1.0+{match.start()}c"
            end   = f"1.0+{match.end()}c"
            t_widget.tag_add(tag, start, end)
def create_editor(parent, path):
    frame = tk.Frame(parent, bg=BG)

    text = tk.Text(
        frame, bg=BG, fg=TEXT, insertbackground=TEXT,
        font=("Consolas", 12),
        undo=True, wrap="word", relief="flat"
    )
    text.pack(fill="both", expand=True)

    text.bind("<Control-z>", lambda e: text.edit_undo())
    text.bind("<Control-y>", lambda e: text.edit_redo())
    text.bind("<Control-c>", lambda e: text.event_generate("<<Copy>>"))
    text.bind("<Control-v>", lambda e: text.event_generate("<<Paste>>"))
    text.bind("<Control-x>", lambda e: text.event_generate("<<Cut>>"))

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text.insert("1.0", f.read())
    highlight(text)
    _after_id = {"id": None}
    def on_change(event=None):
        if _after_id["id"]:
            text.after_cancel(_after_id["id"])
        _after_id["id"] = text.after(200, lambda: highlight(text)) 
    text.bind("<KeyRelease>", on_change)
    return frame

def open_tab(path):
    if os.path.isdir(path):
        return
    if path in tabs:
        notebook.select(tabs[path])
        return

    editor = create_editor(notebook, path)
    notebook.add(editor, text=os.path.basename(path) + "  ×") 
    tabs[path] = editor
    notebook.select(editor)

    notebook.bind("<Button-1>", lambda e: on_tab_click(e))
def on_tab_click(event):
    x, y = event.x, event.y
    elem = notebook.identify(x, y)

    if "label" in elem: 
        index = notebook.index("@%d,%d" % (x, y))
        tab_text = notebook.tab(index, "text")
        if tab_text.endswith("×"):
            frame = notebook.tabs()[index]
            path_to_remove = None
            for p, w in tabs.items():
                if str(w) == frame:
                    path_to_remove = p
                    break
            if path_to_remove:
                notebook.forget(tabs[path_to_remove])
                del tabs[path_to_remove]
def close_tab_by_path(path):
    if path in tabs:
        notebook.forget(tabs[path])
        del tabs[path]

tree.bind("<<TreeviewSelect>>", lambda e:
    open_tab(tree.item(tree.selection()[0], "values")[0])
)

root.bind("<Control-w>", lambda e:
    close_tab_by_path(
        next((p for p, w in tabs.items() if str(w) == notebook.select()), None)
    )
)

refresh_tree()
root.mainloop()