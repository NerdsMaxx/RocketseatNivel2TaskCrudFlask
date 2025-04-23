from typing import Callable

from flask import Flask, request, jsonify
from models.task import Task

app: Flask = Flask(__name__)

tasks: list[Task] = []
task_id_control: int = 1

@app.post('/tasks')
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data['title'], description=data.get('description', ''))
    tasks.append(new_task)
    task_id_control += 1
    for task in tasks:
        print(task)
    return jsonify({"message": "Nova tarefa criada com sucesso", "id": new_task.id})

@app.get('/tasks')
def read_tasks():
    tasks_json: list[dict] = [task.to_dict() for task in tasks]
    return jsonify({
        "tasks": tasks_json,
        "total_tasks": len(tasks_json)
    })

@app.get('/tasks/<int:task_id>')
def get_task(task_id: int):
    task_found: Task | None = find_task(task_id)
    if task_found is None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
        
    return jsonify(task_found.to_dict())
    
@app.put('/tasks/<int:task_id>')
def update_task(task_id: int):
    task_found: Task | None = find_task(task_id)
    if task_found is None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    
    data = request.get_json()
    task_found.title = data['title']
    task_found.description = data['description']
    task_found.completed = data['completed']
    print(task_found)
    
    return jsonify({"message": "Tarefa atualizada com sucesso"})
        
@app.delete('/tasks/<int:task_id>')
def delete_task(task_id: int):
    #global tasks NÃO PRECISA DE GLOBAL, POIS TU SÓ VAI ALTERAR A LISTA EM SI,
    # NÃO TROCAR DE LISTA.
    
    task_found: Task | None = find_task(task_id)
    if task_found is None:
        return jsonify({"message": "Não foi possível encontrar a atividade"}), 404
    
    tasks.remove(task_found)
    return jsonify({"message": "Tarefa deletada com sucesso"})

def find_task(task_id: int) -> Task | None:
    find: Callable[[Task], bool] = lambda t: t.id == task_id
    task_found: Task | None = next(filter(find, tasks), None)
    return task_found

if __name__ == "__main__":
    app.run(debug=True)