#!/usr/bin/env python3
import tkinter as tk
from tkinter import scrolledtext

RESPONSES = {
    "hello": "Hi there!",
    "hi": "Hello!",
    "how are you": "I'm a simple bot — I'm fine, thanks for asking!",
    "bye": "Goodbye! Have a great day!",
    "thanks": "You're welcome!"
}

class ChatbotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Chatbot - Task 4")
        self.geometry("600x420")
        self.create_widgets()

    def create_widgets(self):
        self.chat_area = scrolledtext.ScrolledText(self, state="disabled", wrap="word", height=20)
        self.chat_area.pack(padx=8, pady=8, fill="both", expand=True)
        bottom = tk.Frame(self)
        bottom.pack(fill="x", padx=8, pady=(0,8))
        self.entry = tk.Entry(bottom)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0,6))
        self.entry.bind("<Return>", lambda e: self.send())
        tk.Button(bottom, text="Send", command=self.send).pack(side="right")

        self._say("Bot", "Hi! Type 'hello', 'how are you', 'bye', or similar.")

    def _say(self, who, text):
        self.chat_area.config(state="normal")
        self.chat_area.insert("end", f"{who}: {text}\n")
        self.chat_area.config(state="disabled")
        self.chat_area.see("end")

    def send(self):
        text = self.entry.get().strip()
        self.entry.delete(0, "end")
        if not text:
            return
        self._say("You", text)
        key = text.lower().strip().rstrip("!?")
        response = RESPONSES.get(key, "Sorry, I don't understand. Try 'hello' or 'how are you'.")
        self._say("Bot", response)

if __name__ == '__main__':
    app = ChatbotApp()
    app.mainloop()
