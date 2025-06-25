import click
import json
import datetime
from tabulate import tabulate


def access_tasks(command):
    def set_json(*args, **kwargs):
        try:
            with open("tasks.json", "r") as f:
                json_obj = json.load(f)

        except (FileNotFoundError, json.JSONDecodeError) as error:
            json_obj = {"count":0, "tasks": []}

        changes = command(json_obj, *args, **kwargs)

        with open("tasks.json", "w") as f:
            json.dump(json_obj, f, indent=4)

        return changes
    return set_json


@click.group()
def cli():
    """
    Task tracker cli
    entry command: task-cli
    """
    pass


@cli.command(name="add")
@click.argument("task", type=str)
@access_tasks
def add_task(json_obj, task: str):
    """
    Adds a task to the to-do list
    'task-cli add <task description>'
    """
    
    created = datetime.datetime.now().strftime("%Y - %b %d | %H:%M")

    json_obj["count"] += 1

    task_obj = {
        "description": task,
        "status": "to-do",
        "ID": json_obj["count"],
        "createdAt": created,
        "updatedAT": created
    }
    
    json_obj["tasks"].append(task_obj)

    print("Task added succesfully!")


@cli.command(name="delete")
@click.argument("id", type=int)
@access_tasks
def delete_task(json_obj, id: int):
    if json_obj["tasks"] == []:
        print("There's no tasks in the task list.")
        return None
    
    if json_obj["tasks"][-1]["ID"] < id:
        print("The id doesn't exist in the task database. Check the entire list with the command list")
        return None
    
    for i, t in enumerate(json_obj["tasks"]):
        if t["ID"] == id:
            del json_obj["tasks"][i]
            break
        elif t["ID"] > id:
            print("The id doesn't exist in the task database. Check the entire list with the command: 'list'")
            return None
        
    print("task removed!")


@cli.command(name = "mark")
@click.argument("status", type=str)
@click.argument("id", type=int)
@access_tasks
def mark_task(json_obj, status: str, id: int):

    if status not in ["in-progress", "to-do", "done"]:
        print(f"{status} is not a valid status to mark! Verify if you typed it correctly\nStatus options: 'in-progress', 'to-do' or 'done'.")
        return None

    if id > json_obj["tasks"][-1]["ID"]:
        print(f"Sorry, the id {id} is not a task id on the task list database, check the entire list with the command: 'list'")
        return None

    for t in json_obj["tasks"]:
        if t["ID"] == id:
            t["status"] = status
            break
        elif id < t["ID"]:
            print(f"Sorry, the id {id} is not a task id on the task list database, check the entire list with the command: 'list'")
            return None

    print(f"Task {id} is marked as {status}!")


@cli.command(name="update")
@click.argument("description", type=str)
@click.argument("id", type=int)
@access_tasks
def update_task(json_obj, description: str, id: int):

    if id > json_obj["tasks"][-1]["ID"]:
        print(f"Sorry, the id {id} is not a task id on the task list database, check the entire list with the command: 'list'")
        return None
    
    for t in json_obj["tasks"]:
        if t["ID"] == id:
            t["description"] = description
            t["updatedAT"] = datetime.datetime.now().strftime("%Y - %b %d | %H:%M")
            break
        elif id < t["ID"]:
            print(f"Sorry, the id {id} is not a task id on the task list database, check the entire list with the command: 'list'")
            return None

    print(f"Task {id} updated!")


@cli.command(name="list")
@click.argument("status", type=str, required=False)
@access_tasks
def list_tasks(json_obj, status: str):
    if json_obj["tasks"] == []:
        print("There's no task in the tasks database, you can add taks by typing: add 'task description'")
        return None

    if not status:
        data = [[t["ID"], t["description"], t["status"], t["createdAt"], t["updatedAT"]] for t in json_obj["tasks"]]
    else:
        data = [[t["ID"], t["description"], t["status"], t["createdAt"], t["updatedAT"]] for t in json_obj["tasks"] if t["status"] == status]

    data_head = ["ID", "Description", "Status", "Created at", "Last update"]

    print(tabulate(data, headers=data_head, tablefmt="fancy_grid"))