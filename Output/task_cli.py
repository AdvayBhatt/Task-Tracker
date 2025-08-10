import sys
import json
from datetime import datetime

def helper_function():
   print(
    """
    ## VALID COMMANDS ##
    
    **Adding Task**
    task-cli add "Buy groceries"
    - Output: Task added successfully (ID: 1)

    **Updating and deleting task**
    task-cli update 1 "Buy groceries and cook dinner"
    task-cli delete 1

    **Marking a task as in progress or done**
    task-cli mark-in-progress 1
    task-cli mark-done 1

    **Listing all tasks**
    task-cli list

    **Listing tasks by status**
    task-cli list done
    task-cli list todo
    task-cli list in-progress
    """
   )


#handle when file doesn't exist
file_needed = "data.json"
def load_data():
    data = []
    try:
        with open(file_needed, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        with open(file_needed, "w") as f:
            json.dump([], f)
    return data
    
def dynamic_id_changer(data):
    if not data: #this just means if data is empty
        return 1
    return max(task['id'] for task in data) + 1

def add_task(data):
    creationTime = datetime.now()
    added_data = {"id": dynamic_id_changer(data), "description": sys.argv[2], "status": "todo", "createdAt": creationTime.strftime("%Y-%m-%dT%H:%M:%S"), "updatedAt": creationTime.strftime("%Y-%m-%dT%H:%M:%S")}
    data.append(added_data)
    with open(file_needed, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Task added successfully (ID: {added_data['id']})")

def delete_task(data):
    try:
        int(sys.argv[2])
    except:
        print("Error: Non-integer ID given")
        quit()
    if not data:
        print("No tasks to be deleted!")
        quit()
    found_flag = False
    for entry in data:
        if entry['id'] == int(sys.argv[2]):
            data.remove(entry)
            with open(file_needed, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Task deleted successfully (ID: {entry['id']})")
            found_flag = True
            break

    if not found_flag:
        print("Error: ID given is not valid.")

def update_task(data):
    try:
        int(sys.argv[2])
    except:
        print("Error: Non-integer ID given")
        quit()
    if not data:
        print("No tasks to be updated!")
        quit()
    
    
    found_flag = False
    
    for entry in data:
        if entry['id'] == int(sys.argv[2]):
            entry['description'] = sys.argv[3]
            updateTime = datetime.now()
            entry['updatedAt'] = updateTime.strftime("%Y-%m-%dT%H:%M:%S")
            with open(file_needed, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Task updated successfully (ID: {entry['id']})")
            found_flag = True
            break

    if not found_flag:
        print("Error: ID given is not valid.")

def list_tasks(data):
    try:
        if sys.argv[2] in sys.argv:
            match sys.argv[2]:
                case "done":
                    print("this is done")
                case "todo":
                    print("this is todo")
                case "in-progress":
                    print("this is in-progress")
                case _:
                    print("Error: Not a valid list argument: ", sys.argv[2])
    except:
        print("\n")
        for entry in data:
            created = datetime.strptime(entry['createdAt'], "%Y-%m-%dT%H:%M:%S")
            updated = datetime.strptime(entry['updatedAt'], "%Y-%m-%dT%H:%M:%S")
            
            created_str = created.strftime("%b %d, %Y %I:%M %p")
            updated_str = updated.strftime("%b %d, %Y %I:%M %p")
            
            print(
                f"ID[{entry['id']}]: {entry['description']} is {entry['status']}. "
                f"Created at {created_str}. Updated at {updated_str}.\n"
            )

def mark_task_in_progress(data):
    try:
        int(sys.argv[2])
    except:
        print("Error: Non-integer ID given")
        quit()
    
    found_flag = False
    for entry in data:
        if entry['id'] == int(sys.argv[2]):
            entry['status'] = "in-progress"
            updateTime = datetime.now()
            entry['updatedAt'] = updateTime.strftime("%Y-%m-%dT%H:%M:%S")
            with open(file_needed, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Task marked as in-progress (ID: {entry['id']})")
            found_flag = True
            break

    if not found_flag:
        print("Error: ID given is not valid.") 


def mark_task_done(data):
    try:
        int(sys.argv[2])
    except:
        print("Error: Non-integer ID given")
        quit()
    
    found_flag = False
    for entry in data:
        if entry['id'] == int(sys.argv[2]):
            entry['status'] = "done"
            updateTime = datetime.now()
            entry['updatedAt'] = updateTime.strftime("%Y-%m-%dT%H:%M:%S")
            with open(file_needed, "w") as f:
                json.dump(data, f, indent=4)
            print(f"Task marked as done (ID: {entry['id']})")
            found_flag = True
            break

    if not found_flag:
        print("Error: ID given is not valid.") 
    

def tasks():
    if len(sys.argv) < 2:
        print("Error: No command provided.")
        quit()
    match sys.argv[1]:
        case "add":
            if len(sys.argv) < 3:
                print("Error: Incomplete 'add' command.")
                quit()
            tasks_data = load_data()
            add_task(tasks_data)
        case "delete":
            if len(sys.argv) < 3:
                print("Error: Incomplete 'delete' command!")
                quit()
            tasks_data = load_data()
            delete_task(tasks_data)
        case "update":
            if len(sys.argv) < 4:
                print("Error: Incomplete 'update' command!")
                quit()
            tasks_data = load_data()
            update_task(tasks_data) 
        case "mark-in-progress":
            tasks_data = load_data()
            mark_task_in_progress(tasks_data)
            
        case "mark-done":
            tasks_data = load_data()
            mark_task_done(tasks_data)
        case "list":
            tasks_data = load_data()
            list_tasks(tasks_data)
        case "help":
            helper_function()
        case _:
            print("Not a valid secondary command: ", sys.argv[1])

if __name__ == "__main__":
    tasks()