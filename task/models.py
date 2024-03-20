# app/models.py
from task import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)

    def __init__(self, name, description, due_date):
        self.name = name
        self.description = description
        self.due_date = due_date

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'due_date': self.due_date.strftime('%d-%m-%Y') if self.due_date else None
        }
