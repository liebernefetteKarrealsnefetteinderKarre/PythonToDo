import tkinter as tk
from tkinter import messagebox
import random

class Character:
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
        self.level = 1
        self.xp = 0

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            return True  # Level-Up erfolgt
        return False

class ToDoGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo Adventure")
        self.root.geometry("500x650")

        self.characters = [
            Character("Krieger", "🗡️"),
            Character("Magier", "🪄"),
            Character("Bogenschütze", "🏹")
        ]
        self.selected_character = None

        self.character_label = tk.Label(root, text="Wähle deinen Charakter:", font=("Helvetica", 14))
        self.character_label.pack(pady=10)

        self.character_buttons = []
        for char in self.characters:
            btn = tk.Button(root, text=f"{char.icon} {char.name}", width=20, command=lambda c=char: self.select_character(c))
            btn.pack(pady=5)
            self.character_buttons.append(btn)

        self.status_label = tk.Label(root, text="Keine Aufgabe aktiv", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.level_label = tk.Label(root, text="Level: 0 | XP: 0", font=("Helvetica", 12))
        self.level_label.pack(pady=5)

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Quest hinzufügen", width=20, command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

        self.complete_button = tk.Button(root, text="Quest abschließen", width=20, command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Quest löschen", width=20, command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.reminder_button = tk.Button(root, text="Erinnerung anzeigen", width=20, command=self.set_reminder)
        self.reminder_button.pack(pady=5)

    def select_character(self, character):
        self.selected_character = character
        self.update_status()
        for btn in self.character_buttons:
            btn.config(state=tk.DISABLED)

    def update_status(self):
        if self.selected_character:
            self.status_label.config(text=f"{self.selected_character.icon} {self.selected_character.name} bereit für Abenteuer!")
            self.level_label.config(text=f"Level: {self.selected_character.level} | XP: {self.selected_character.xp}")

    def add_task(self):
        task = self.task_entry.get()
        if task and self.selected_character:
            self.task_listbox.insert(tk.END, f"{self.selected_character.icon} {task}")
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warnung", "Bitte wähle einen Charakter und gib eine Quest ein.")

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index and self.selected_character:
            task = self.task_listbox.get(selected_task_index)
            self.task_listbox.delete(selected_task_index)
            self.task_listbox.insert(tk.END, f"✔️ {task} abgeschlossen!")
            leveled_up = self.selected_character.gain_xp(50)
            self.update_status()
            if leveled_up:
                messagebox.showinfo("Level Up!", f"{self.selected_character.name} hat Level {self.selected_character.level} erreicht!")
        else:
            messagebox.showwarning("Warnung", "Bitte eine Quest auswählen.")

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            self.task_listbox.delete(selected_task_index)
        else:
            messagebox.showwarning("Warnung", "Bitte eine Quest auswählen.")

    def set_reminder(self):
        reminders = [
            "Ein Held ruht nie! Mach weiter!",
            "Dein Abenteuer wartet!",
            "Keine Zeit zu verlieren, Kämpfer!"
        ]
        messagebox.showinfo("Erinnerung", random.choice(reminders))

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoGameApp(root)
    root.mainloop()
