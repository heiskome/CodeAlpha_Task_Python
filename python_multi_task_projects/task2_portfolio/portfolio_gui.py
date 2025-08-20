#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import csv
from datetime import datetime

PRICES = {
    "AAPL": 180,
    "TSLA": 250,
    "MSFT": 300,
    "GOOG": 125,
    "AMZN": 100
}

class PortfolioApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Portfolio Tracker - Task 2")
        self.geometry("650x420")
        self.create_widgets()
        self.holdings = []

    def create_widgets(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        # --- Dropdown for stock selection ---
        ttk.Label(frm, text="Stock (ticker):").grid(row=0, column=0, sticky="w")
        self.stock_var = tk.StringVar()
        self.stock_combo = ttk.Combobox(frm, textvariable=self.stock_var, values=list(PRICES.keys()), state="readonly", width=12)
        self.stock_combo.grid(row=0, column=1, sticky="w")
        self.stock_combo.set("AAPL")  # default value

        ttk.Label(frm, text="Quantity:").grid(row=0, column=2, sticky="w", padx=(12,0))
        self.qty_entry = ttk.Entry(frm, width=8)
        self.qty_entry.grid(row=0, column=3, sticky="w")

        ttk.Button(frm, text="Add", command=self.add_holding).grid(row=0, column=4, padx=8)
        ttk.Button(frm, text="Save CSV", command=self.save_csv).grid(row=0, column=5, padx=8)

        # --- Table for portfolio ---
        self.tree = ttk.Treeview(frm, columns=("Ticker","Qty","Price","Value"), show="headings", height=12)
        for c in ("Ticker","Qty","Price","Value"):
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=6, pady=(10,0), sticky="nsew")

        frm.rowconfigure(1, weight=1)
        frm.columnconfigure(5, weight=1)

        self.total_var = tk.StringVar(value="Total Investment: 0")
        ttk.Label(frm, textvariable=self.total_var, font=("Helvetica", 12, "bold")).grid(row=2, column=0, columnspan=6, pady=8)

        ttk.Label(frm, text="Price Dictionary:").grid(row=3, column=0, sticky="w", pady=(6,0))
        ttk.Label(frm, text=str(PRICES)).grid(row=4, column=0, columnspan=6, sticky="w")

    def add_holding(self):
        ticker = self.stock_var.get().strip().upper()
        try:
            qty = float(self.qty_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid", "Quantity must be a number.")
            return

        price = PRICES.get(ticker)
        if price is None:
            if messagebox.askyesno("Unknown ticker", f"{ticker} not in price list. Add with manual price?"):
                p = simpledialog.askfloat("Manual Price", f"Enter price for {ticker}:")
                if p is None:
                    return
                price = p
                PRICES[ticker] = price
                # update dropdown options
                self.stock_combo["values"] = list(PRICES.keys())
            else:
                return

        value = qty * price
        self.holdings.append((ticker, qty, price, value))
        self.refresh_table()

        # --- Reset quantity field for next entry ---
        self.qty_entry.delete(0, "end")

    def refresh_table(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        total = 0
        for h in self.holdings:
            self.tree.insert("", "end", values=(h[0], h[1], h[2], h[3]))
            total += h[3]
        self.total_var.set(f"Total Investment: {total:.2f}")

    def save_csv(self):
        if not self.holdings:
            messagebox.showinfo("No data", "No holdings to save.")
            return
        f = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not f:
            return
        with open(f, "w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["Ticker","Quantity","Price","Value","SavedAt"])
            for t,q,p,v in self.holdings:
                writer.writerow([t,q,p,v, datetime.utcnow().isoformat()])
        messagebox.showinfo("Saved", f"Holdings saved to {f}")

if __name__ == '__main__':
    app = PortfolioApp()
    app.mainloop()
