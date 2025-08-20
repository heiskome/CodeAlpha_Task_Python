#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, shutil

class MoverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Mover - Task 3 (Automation)")
        self.geometry("600x260")
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Move all .jpg files from source to destination").grid(row=0, column=0, columnspan=3, pady=(0,8))

        ttk.Label(frm, text="Source folder:").grid(row=1, column=0, sticky="w")
        self.src_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.src_var, width=48).grid(row=1, column=1)
        ttk.Button(frm, text="Browse", command=self.browse_src).grid(row=1, column=2, padx=6)

        ttk.Label(frm, text="Destination folder:").grid(row=2, column=0, sticky="w")
        self.dst_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.dst_var, width=48).grid(row=2, column=1)
        ttk.Button(frm, text="Browse", command=self.browse_dst).grid(row=2, column=2, padx=6)

        ttk.Button(frm, text="Move .jpg files", command=self.move_jpgs).grid(row=3, column=0, columnspan=3, pady=12)

        self.log = tk.Text(frm, height=6)
        self.log.grid(row=4, column=0, columnspan=3, sticky="nsew")
        frm.rowconfigure(4, weight=1)

    def browse_src(self):
        d = filedialog.askdirectory()
        if d: self.src_var.set(d)

    def browse_dst(self):
        d = filedialog.askdirectory()
        if d: self.dst_var.set(d)

    def move_jpgs(self):
        s = self.src_var.get().strip()
        d = self.dst_var.get().strip()
        if not (s and d):
            messagebox.showerror("Missing", "Please select both source and destination folders.")
            return
        if not os.path.isdir(s):
            messagebox.showerror("Invalid", "Source is not a folder.")
            return
        os.makedirs(d, exist_ok=True)
        moved = 0
        for fname in os.listdir(s):
            if fname.lower().endswith(".jpg"):
                try:
                    shutil.move(os.path.join(s, fname), os.path.join(d, fname))
                    self.log.insert("end", f"Moved: {fname}\n")
                    moved += 1
                except Exception as e:
                    self.log.insert("end", f"Failed: {fname} -> {e}\n")
        self.log.insert("end", f"Done. Total moved: {moved}\n")
        messagebox.showinfo("Done", f"Total moved: {moved} files.")

if __name__ == '__main__':
    app = MoverApp()
    app.mainloop()