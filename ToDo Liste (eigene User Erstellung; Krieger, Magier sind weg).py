import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class User:
    def __init__(self, username):
        self.username = username

class ToDoGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ToDo Adventure")
        self.root.geometry("600x850")

        self.users = []
        self.selected_user = None

        self.user_frame = tk.Frame(root)
        self.user_frame.pack(pady=10)

        self.username_entry = tk.Entry(self.user_frame, width=20)
        self.username_entry.grid(row=0, column=0, padx=5)

        self.add_user_button = tk.Button(self.user_frame, text="Benutzer hinzufügen", command=self.add_user)
        self.add_user_button.grid(row=0, column=1, padx=5)

        self.user_listbox = tk.Listbox(root, width=40, height=5)
        self.user_listbox.pack(pady=5)
        self.user_listbox.bind('<<ListboxSelect>>', self.select_user)

        self.status_label = tk.Label(root, text="Keine Aufgabe aktiv", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)

        self.due_date_entry = tk.Entry(root, width=40)
        self.due_date_entry.pack(pady=5)
        self.due_date_entry.insert(0, "Fälligkeitsdatum (TT.MM.JJJJ)")

        self.status_var = tk.StringVar(value="Nicht aktiv")
        self.status_menu = tk.OptionMenu(root, self.status_var, "Nicht aktiv", "In Bearbeitung", "Erledigt")
        self.status_menu.pack(pady=5)

        self.difficulty_var = tk.StringVar(value="Leicht")
        self.difficulty_menu = tk.OptionMenu(root, self.difficulty_var, "Leicht", "Mittel", "Schwer")
        self.difficulty_menu.pack(pady=5)

        self.add_button = tk.Button(root, text="Quest hinzufügen", width=20, command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, width=70, height=15, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

    def add_user(self):
        username = self.username_entry.get()
        if username:
            self.users.append(User(username))
            self.user_listbox.insert(tk.END, username)
            self.username_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warnung", "Bitte Benutzername eingeben.")

    def select_user(self, event):
        index = self.user_listbox.curselection()
        if index:
            self.selected_user = self.users[index[0]]
            messagebox.showinfo("Benutzer ausgewählt", f"{self.selected_user.username} wurde ausgewählt.")

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.due_date_entry.get()
        if not task or not due_date:
            messagebox.showwarning("Warnung", "Bitte Aufgabe und Fälligkeitsdatum eingeben.")
            return
        self.task_listbox.insert(tk.END, f"{task} | Fällig: {due_date} | Status: {self.status_var.get()} | Schwierigkeit: {self.difficulty_var.get()}")
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoGameApp(root)
    root.mainloop()
