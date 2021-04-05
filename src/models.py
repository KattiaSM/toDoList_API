from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ToDoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), unique=True, nullable=False)
    done = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<ToDoList %r>' % self.task

    def serialize(self):
        return {
            "id": self.id,
            "task": self.task,
            # do not serialize the password, its a security breach
        }