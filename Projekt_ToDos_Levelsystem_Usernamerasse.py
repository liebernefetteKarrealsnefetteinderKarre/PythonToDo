import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import random

class Character:
    def __init__(self, name, race, age):
        self.name = name
        self.race = race
        self.age = age
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
        self.root.geometry("600x800")

        self.characters = []
        self.selected_character = None

        self.create_character_button = tk.Button(root, text="Benutzer erstellen", width=20, command=self.open_create_character_window)
        self.create_character_button.pack(pady=10)

        self.character_label = tk.Label(root, text="Wähle deinen Charakter:", font=("Helvetica", 14))
        self.character_label.pack(pady=10)

        self.character_buttons_frame = tk.Frame(root)
        self.character_buttons_frame.pack(pady=10)

        self.status_label = tk.Label(root, text="Keine Aufgabe aktiv", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.level_label = tk.Label(root, text="Level: 0 | XP: 0", font=("Helvetica", 12))
        self.level_label.pack(pady=5)

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=5)

        self.difficulty_label = tk.Label(root, text="Schwierigkeitsgrad:")
        self.difficulty_label.pack(pady=5)
        self.difficulty_var = tk.StringVar(value="Einfach")
        self.difficulty_menu = tk.OptionMenu(root, self.difficulty_var, "Einfach", "Mittel", "Schwer")
        self.difficulty_menu.pack(pady=5)

        self.due_date_label = tk.Label(root, text="Fälligkeitsdatum (YYYY-MM-DD):")
        self.due_date_label.pack(pady=5)
        self.due_date_entry = tk.Entry(root, width=20)
        self.due_date_entry.pack(pady=5)

        self.add_button = tk.Button(root, text="Quest hinzufügen", width=20, command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, width=70, height=15, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

        self.complete_button = tk.Button(root, text="Quest abschließen", width=20, command=self.complete_task)
        self.complete_button.pack(pady=5)

        self.in_progress_button = tk.Button(root, text="Status: In Arbeit", width=20, command=self.mark_task_in_progress)
        self.in_progress_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Quest löschen", width=20, command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.reminder_button = tk.Button(root, text="Erinnerung anzeigen", width=20, command=self.set_reminder)
        self.reminder_button.pack(pady=5)

    def open_create_character_window(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Benutzer erstellen")
        create_window.geometry("400x300")

        tk.Label(create_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(create_window)
        name_entry.pack(pady=5)

        tk.Label(create_window, text="Alter:").pack(pady=5)
        age_entry = tk.Entry(create_window)
        age_entry.pack(pady=5)

        tk.Label(create_window, text="Rasse:").pack(pady=5)
        race_entry = tk.Entry(create_window)
        race_entry.pack(pady=5)

        def create_character():
            name = name_entry.get()
            age = age_entry.get()
            race = race_entry.get()

            if name and age.isdigit() and race:
                new_character = Character(name, race, int(age))
                self.characters.append(new_character)
                self.update_character_buttons()
                create_window.destroy()
            else:
                messagebox.showwarning("Warnung", "Bitte gültige Daten eingeben.")

        tk.Button(create_window, text="Erstellen", command=create_character).pack(pady=10)

    def update_character_buttons(self):
        for widget in self.character_buttons_frame.winfo_children():
            widget.destroy()

        for char in self.characters:
            btn = tk.Button(self.character_buttons_frame, text=f"{char.name} ({char.race}, {char.age} Jahre)", width=30, command=lambda c=char: self.select_character(c))
            btn.pack(pady=5)

    def select_character(self, character):
        self.selected_character = character
        self.update_status()
        for btn in self.character_buttons_frame.winfo_children():
            btn.config(state=tk.DISABLED)

    def update_status(self):
        if self.selected_character:
            self.status_label.config(text=f"{self.selected_character.name} ({self.selected_character.race}) bereit für Abenteuer!")
            self.level_label.config(text=f"Level: {self.selected_character.level} | XP: {self.selected_character.xp}")

    def add_task(self):
        task = self.task_entry.get()
        difficulty = self.difficulty_var.get()
        due_date_str = self.due_date_entry.get()

        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Warnung", "Bitte ein gültiges Fälligkeitsdatum eingeben (YYYY-MM-DD).")
            return

        if task and self.selected_character:
            self.task_listbox.insert(tk.END, f"{task} | Schwierigkeit: {difficulty} | Fällig: {due_date_str} | Status: Nicht begonnen")
            self.task_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warnung", "Bitte wähle einen Charakter und gib eine Quest ein.")

    def complete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index and self.selected_character:
            task = self.task_listbox.get(selected_task_index)
            parts = task.split(" | ")
            if "Status: Abgeschlossen" not in task:
                # XP-Belohnung basierend auf Schwierigkeit
                difficulty = parts[1].replace("Schwierigkeit: ", "").strip()
                if difficulty == "Einfach":
                    xp_reward = 10
                elif difficulty == "Mittel":
                    xp_reward = 30
                elif difficulty == "Schwer":
                    xp_reward = 50
                else:
                    xp_reward = 0  # Sicherheitswert, falls Schwierigkeit nicht erkennbar ist
                
                updated_task = f"{parts[0]} | {parts[1]} | {parts[2]} | Status: Abgeschlossen"
                self.task_listbox.delete(selected_task_index)
                self.task_listbox.insert(tk.END, updated_task)
                leveled_up = self.selected_character.gain_xp(xp_reward)
                self.update_status()
                if leveled_up:
                    messagebox.showinfo("Level Up!", f"{self.selected_character.name} hat Level {self.selected_character.level} erreicht!")
            else:
                messagebox.showwarning("Warnung", "Diese Quest ist bereits abgeschlossen.")
        else:
            messagebox.showwarning("Warnung", "Bitte eine Quest auswählen.")

    def mark_task_in_progress(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.task_listbox.get(selected_task_index)
            parts = task.split(" | ")
            if "Status: In Arbeit" not in task and "Status: Abgeschlossen" not in task:
                updated_task = f"{parts[0]} | {parts[1]} | {parts[2]} | Status: In Arbeit"
                self.task_listbox.delete(selected_task_index)
                self.task_listbox.insert(tk.END, updated_task)
            else:
                messagebox.showwarning("Warnung", "Diese Quest ist bereits in Arbeit oder abgeschlossen.")
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

    def check_task_status(self):
        now = datetime.now()
        for i in range(self.task_listbox.size()):
            task = self.task_listbox.get(i)
            parts = task.split(" | ")
            due_date_str = parts[2].replace("Fällig: ", "")
            status = parts[3].replace("Status: ", "")
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
                if now > due_date and "Abgeschlossen" not in status:
                    updated_task = f"{parts[0]} | {parts[1]} | {parts[2]} | Status: Abgelaufen"
                    self.task_listbox.delete(i)
                    self.task_listbox.insert(i, updated_task)
            except ValueError:
                continue

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoGameApp(root)
    root.mainloop()
