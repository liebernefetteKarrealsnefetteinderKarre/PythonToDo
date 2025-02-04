from nicegui import ui
from datetime import datetime
import sqlite3

class Character:
    def __init__(self, name, race, age, level=1, xp=0):
        self.name = name
        self.race = race
        self.age = age
        self.level = level
        self.xp = xp

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.level * 100:
            self.xp -= self.level * 100
            self.level += 1
            return True  # Level-Up erfolgt
        return False

class ToDoGameApp:
    def __init__(self):
        self.characters = []
        self.selected_character = None
        self.tasks = []

    def start(self):
        self.character_buttons_frame = ui.column()
        self.task_list_frame = ui.column()
        self.load_data()

        with ui.row():
            ui.button("Benutzer erstellen", on_click=self.open_create_character_window)
            self.status_label = ui.label("Keine Aufgabe aktiv")
            self.level_label = ui.label("Level: 0 | XP: 0")

        ui.separator()
        self.update_character_buttons()
        
        with ui.row():
            self.task_entry = ui.input(label="Neue Aufgabe").classes("w-1/3")
            self.difficulty_dropdown = ui.select(["Einfach", "Mittel", "Schwer"], value="Einfach", label="Schwierigkeitsgrad")
            self.due_date_entry = ui.input(label="Fälligkeitsdatum (YYYY-MM-DD)")

        ui.button("Quest hinzufügen", on_click=self.add_task)
        ui.button("Quest abschließen", on_click=self.complete_task)
        ui.button("Status: In Arbeit", on_click=self.mark_task_in_progress)
        ui.button("Quest löschen", on_click=self.delete_task)
        ui.button("Erinnerung anzeigen", on_click=self.set_reminder)

        with ui.card():
            self.task_list = ui.column()

    def load_data(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("SELECT name, race, age FROM characters")
        rows = cursor.fetchall()
        self.characters = [Character(name, race, age) for name, race, age in rows]
        
        connection.close()
        self.update_character_buttons()
    
    def update_character_buttons(self):
        self.character_buttons_frame.clear()
        if not self.characters:
            self.character_buttons_frame.clear()
            self.character_buttons_frame.append(ui.label("Keine Benutzer vorhanden.").classes("text-red-500"))
        else:
            for character in self.characters:
                self.character_buttons_frame.append(
                    ui.button(character.name, on_click=lambda c=character: self.select_character(c)).classes("w-full")
                )
    
    def select_character(self, character):
        self.selected_character = character
        self.status_label.set_text(f"Aktiver Charakter: {character.name}")
        self.level_label.set_text(f"Level: {character.level} | XP: {character.xp}")
    
    def add_task(self):
        task = self.task_entry.value
        difficulty = self.difficulty_dropdown.value
        due_date_str = self.due_date_entry.value

        try:
            datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            ui.notify("Bitte ein gültiges Fälligkeitsdatum eingeben (YYYY-MM-DD).", color="red")
            return

        if task and self.selected_character:
            self.tasks.append((task, difficulty, due_date_str, "Nicht begonnen"))
            self.update_task_list()
        else:
            ui.notify("Bitte wähle einen Charakter und gib eine Quest ein.", color="red")
    
    def complete_task(self):
        ui.notify("Quest abgeschlossen!", color="green")
    
    def mark_task_in_progress(self):
        ui.notify("Quest als 'In Arbeit' markiert!", color="blue")
    
    def delete_task(self):
        ui.notify("Quest gelöscht!", color="red")
    
    def set_reminder(self):
        ui.notify("Erinnerung gesetzt!", color="yellow")
    
    def update_task_list(self):
        self.task_list.clear()
    
    def save_character_to_db(self, character):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO characters (name, race, age) VALUES (?, ?, ?)", (character.name, character.race, character.age))
        connection.commit()
        connection.close()
        self.load_data()

    def open_create_character_window(self):
        with ui.dialog() as dialog, ui.card():
            name_input = ui.input(label="Name")
            age_input = ui.input(label="Alter")
            race_input = ui.input(label="Rasse")
            ui.button("Erstellen", on_click=lambda: self.create_character(name_input.value, age_input.value, race_input.value, dialog))
            ui.button("Abbrechen", on_click=dialog.close)
        dialog.open()

    def create_character(self, name, age, race, dialog):
        if name and age.isdigit() and race:
            new_character = Character(name, race, int(age))
            self.characters.append(new_character)
            self.save_character_to_db(new_character)
            dialog.close()
        else:
            ui.notify("Bitte gültige Daten eingeben.", color="red")

app = ToDoGameApp()
app.start()
ui.run()
