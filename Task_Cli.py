import sys
import json
import os
from datetime import datetime

# JSON file to store tasks
task_file = "tasks.json"

def load_tasks():
    if not os.path.exists(task_file):
        return []
    with open(task_file, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(task_file, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task(description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print("Task updated successfully")
            return
    print("Task not found")

def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    print("Task deleted successfully")

def mark_task(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task marked as {status}")
            return
    print("Task not found")

def list_tasks(status=None):
    tasks = load_tasks()
    filtered_tasks = [task for task in tasks if status is None or task["status"] == status]
    if not filtered_tasks:
        print("No tasks found")
    else:
        for task in filtered_tasks:
            print(f"{task['id']}: {task['description']} [{task['status']}]")

def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return
    
    command = sys.argv[1]
    if command == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif command == "update" and len(sys.argv) > 3:
        update_task(int(sys.argv[2]), " ".join(sys.argv[3:]))
    elif command == "delete" and len(sys.argv) > 2:
        delete_task(int(sys.argv[2]))
    elif command == "mark-in-progress" and len(sys.argv) > 2:
        mark_task(int(sys.argv[2]), "in-progress")
    elif command == "mark-done" and len(sys.argv) > 2:
        mark_task(int(sys.argv[2]), "done")
    elif command == "list":
        if len(sys.argv) > 2:
            list_tasks(sys.argv[2])
        else:
            list_tasks()
    else:
        print("Invalid command or missing arguments")

if __name__ == "__main__":
    main()
