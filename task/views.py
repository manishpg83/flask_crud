# app/views.py
from flask import redirect, render_template, jsonify, request
from task import app, db
from task.models import Task
from sqlalchemy.exc import IntegrityError
from datetime import datetime

@app.before_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        if not all(key in data for key in ['name', 'description', 'due_date']):
            return jsonify({'error': 'Missing required fields'}), 400

        name = data['name']
        description = data['description']
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')

        new_task = Task(name=name, description=description, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()

        return jsonify({'message': 'Task added successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Task already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/tasks')
def show_tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    serialized_tasks = [task.serialize() for task in tasks]
    return jsonify(serialized_tasks)


@app.route('/data/<int:id>/update', methods=['POST'])
def update_task(id):
    task = Task.query.get_or_404(id)
    task.name = request.form['name']
    task.description = request.form['description']
    task.due_date = request.form['due_date']

    try:
        db.session.commit()
        return jsonify({"message": "Task updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error updating task: {e}"}), 500

@app.route('/data/<int:id>/delete', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/tasks')  # Redirect to the main tasks page
    except Exception as e:
        db.session.rollback()
        return f"Error deleting task: {e}", 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({'error': 'Method Not Allowed'}), 405


@app.route('/tasks/<int:id>/update', methods=['GET'])
def render_update_task_form(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return render_template('update.html', task=task)