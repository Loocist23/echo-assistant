import sqlite3
import datetime


class TaskManager:
    def __init__(self, db_path="tasks.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """
        Initialise la base de données si elle n'existe pas.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    reminder_time DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_task(self, task, reminder_time=None):
        """
        Ajoute une tâche avec une heure de rappel optionnelle.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (task, reminder_time) VALUES (?, ?)
            ''', (task, reminder_time))
            conn.commit()
        return "Tâche ajoutée avec succès."

    def list_tasks(self):
        """
        Liste toutes les tâches.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT task, reminder_time FROM tasks')
            tasks = cursor.fetchall()

        if not tasks:
            return "Aucune tâche en cours."
        return "\n".join([f"- {task} (rappel : {reminder_time})" for task, reminder_time in tasks])

    def remove_task(self, task_name):
        """
        Supprime une tâche spécifique par son nom.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM tasks WHERE task = ?
            ''', (task_name,))
            conn.commit()
        return f"Tâche '{task_name}' supprimée."

    def check_reminders(self):
        """
        Vérifie les rappels et renvoie les tâches à rappeler.
        Ne supprime que les tâches ayant un `reminder_time`.
        """
        now = datetime.datetime.now()
        reminders = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, task FROM tasks 
                WHERE reminder_time IS NOT NULL AND reminder_time <= ?
            ''', (now,))
            reminders = cursor.fetchall()

            # Supprime uniquement les tâches avec un `reminder_time`
            cursor.executemany('''
                DELETE FROM tasks WHERE id = ?
            ''', [(task_id,) for task_id, _ in reminders])
            conn.commit()

        return [task for _, task in reminders]

