from datetime import datetime


class Task:
    def __init__(self, id, description, status="To Do", creation_date=None):
        self.id = id
        self.description = description
        self.status = status
        # Keep a consistent string timestamp for JSON storage and display.
        self.creation_date = creation_date or datetime.now().isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "creation_date": self.creation_date,
        }
