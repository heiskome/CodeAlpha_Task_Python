#!/usr/bin/env python3
import random
import tkinter as tk
from tkinter import messagebox

WORDS = ["python", "hangman", "developer", "widget", "notebook"]

class HangmanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman - Task 1")
        self.geometry("600x400")
        self.resizable(False, False)
        self.font = ("Helvetica", 14)
        self.reset_game()
        self.create_widgets()

    def reset_game(self):
        self.secret = random.choice(WORDS)
        self.guessed = set()
        self.wrong = 0
        self.max_wrong = 6

    def create_widgets(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack(side="left", fill="y")

        tk.Label(frame, text="Hangman", font=("Helvetica", 18, "bold")).pack(pady=(0,8))

        self.word_var = tk.StringVar(value=self.display_word())
        tk.Label(frame, textvariable=self.word_var, font=self.font).pack(pady=8)

        tk.Label(frame, text="Enter a letter:", font=self.font).pack()
        self.entry = tk.Entry(frame, font=self.font, width=4, justify="center")
        self.entry.pack(pady=6)
        self.entry.bind("<Return>", lambda e: self.guess())

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=6)
        tk.Button(btn_frame, text="Guess", command=self.guess).pack(side="left", padx=6)
        tk.Button(btn_frame, text="New Game", command=self.new_game).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Quit", command=self.quit).pack(side="left", padx=6)

        self.status_var = tk.StringVar(value=f"Wrong: {self.wrong}/{self.max_wrong}")
        tk.Label(frame, textvariable=self.status_var, font=self.font).pack(pady=6)

        self.hint_var = tk.StringVar(value="Guessed: ")
        tk.Label(frame, textvariable=self.hint_var).pack(pady=2)

        # Canvas for stickman
        self.canvas = tk.Canvas(self, width=250, height=350, bg="white")
        self.canvas.pack(side="right", padx=10, pady=10)
        self.draw_base()

    def display_word(self):
        return " ".join([c if c in self.guessed else "_" for c in getattr(self, "secret", "")])

    def guess(self):
        letter = self.entry.get().strip().lower()
        self.entry.delete(0, "end")
        if not letter or len(letter) != 1 or not letter.isalpha():
            messagebox.showinfo("Invalid", "Please enter a single alphabetic character.")
            return
        if letter in self.guessed:
            messagebox.showinfo("Info", f"You already guessed '{letter}'.")
            return
        if letter in self.secret:
            self.guessed.add(letter)
        else:
            self.guessed.add(letter)
            self.wrong += 1
            self.draw_hangman()
        self.word_var.set(self.display_word())
        self.status_var.set(f"Wrong: {self.wrong}/{self.max_wrong}")
        self.hint_var.set("Guessed: " + ", ".join(sorted(self.guessed)))
        self.check_game_over()

    def check_game_over(self):
        if all(c in self.guessed for c in self.secret):
            messagebox.showinfo("Victory", f"Congratulations — you guessed the word: {self.secret}")
            self.new_game()
        elif self.wrong >= self.max_wrong:
            messagebox.showinfo("Game Over", f"You lost. The word was: {self.secret}")
            self.new_game()

    def new_game(self):
        self.reset_game()
        self.word_var.set(self.display_word())
        self.status_var.set(f"Wrong: {self.wrong}/{self.max_wrong}")
        self.hint_var.set("Guessed: ")
        self.canvas.delete("all")
        self.draw_base()

    # --- Stickman drawing ---
    def draw_base(self):
        """Draw gallows base"""
        self.canvas.create_line(20, 330, 200, 330, width=4)   # ground
        self.canvas.create_line(60, 330, 60, 50, width=4)     # pole
        self.canvas.create_line(60, 50, 160, 50, width=4)     # top beam
        self.canvas.create_line(160, 50, 160, 80, width=4)    # rope

    def draw_hangman(self):
        """Draw next part of stickman"""
        parts = [
            lambda: self.canvas.create_oval(140, 80, 180, 120, width=3),             # head
            lambda: self.canvas.create_line(160, 120, 160, 200, width=3),            # body
            lambda: self.canvas.create_line(160, 140, 130, 170, width=3),            # left arm
            lambda: self.canvas.create_line(160, 140, 190, 170, width=3),            # right arm
            lambda: self.canvas.create_line(160, 200, 140, 250, width=3),            # left leg
            lambda: self.canvas.create_line(160, 200, 180, 250, width=3)             # right leg
        ]
        if self.wrong <= len(parts):
            parts[self.wrong-1]()  # draw next part


if __name__ == '__main__':
    app = HangmanApp()
    app.mainloop()
