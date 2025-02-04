import sqlite3

def setup_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    try:
        # Tabelle für Benutzer
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            race TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        ''')

        # Neue Tabelle für Charaktere
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            race TEXT NOT NULL,
            age INTEGER NOT NULL,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

        # Angepasste Tabelle für Aufgaben
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            time_create DATE NOT NULL,
            time_finish DATE NOT NULL,
            priority TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Nicht begonnen',
            character_id INTEGER,
            FOREIGN KEY (character_id) REFERENCES characters(id)
        )
        ''')
        
        print("Datenbanktabellen wurden erfolgreich erstellt oder existieren bereits.")
    except sqlite3.Error as e:
        print(f"Fehler beim Erstellen der Tabellen: {e}")
    
    connection.commit()
    connection.close()
    print("Datenbankverbindung geschlossen.")

# Datenbank initialisieren
if __name__ == "__main__":
    setup_database()
    print("Datenbank wurde erfolgreich aktualisiert.")
