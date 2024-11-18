import datetime

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task, reminder_time=None):
        """
        Ajoute une tâche avec une heure de rappel optionnelle.
        """
        task_entry = {"task": task, "reminder_time": reminder_time, "created_at": datetime.datetime.now()}
        self.tasks.append(task_entry)
        return "Tâche ajoutée avec succès."

    def list_tasks(self):
        """
        Liste toutes les tâches.
        """
        if not self.tasks:
            return "Aucune tâche en cours."
        return "\n".join([f"- {task['task']} (rappel : {task['reminder_time']})" for task in self.tasks])

    def remove_task(self, task_name):
        """
        Supprime une tâche spécifique par son nom.
        """
        self.tasks = [task for task in self.tasks if task['task'] != task_name]
        return f"Tâche '{task_name}' supprimée."

    def check_reminders(self):
        """
        Vérifie les rappels et renvoie les tâches à rappeler.
        """
        now = datetime.datetime.now()
        reminders = [task for task in self.tasks if task["reminder_time"] and task["reminder_time"] <= now]
        for task in reminders:
            self.tasks.remove(task)  # Suppression après le rappel
        return reminders
