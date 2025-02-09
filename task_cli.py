import json
import datetime
import argparse


data = {}
data_temp = {}
idx = 0
with open('task_manager.json', 'r', encoding='utf-8') as f:
    try:
        data_temp = json.load(f)
        for id, task in data_temp.items():
            data[idx] = task
            idx = idx + 1
    except Exception as e:
        print(e)
        idx = 0
def refresh():
    with open('task_manager.json', 'w', encoding='utf-8') as f:
        id_temp = 0
        temp = {}
        for id, task in data.items():
            temp[id_temp] = task
            id_temp = id_temp + 1
        json.dump(temp, f, indent=4)

def add(task):
    result = [task, 'todo', str(datetime.datetime.now()), str(datetime.datetime.now())]
    data[idx] = result
    refresh()

def update(id,new_task):
    id = int(id)
    temp = data[id]
    temp[0] = new_task
    temp[-1] = str(datetime.datetime.now())
    data[id] = temp
    refresh()

def delete(id):
    del data[id]
    refresh()

def mark_in_progress(id:int):
    temp = data[id]
    temp[1] = 'in-progress'
    data[id] = temp
    refresh()

def mark_done(id:int):
    print(type(id))
    temp = data[id]
    temp[1] = 'done'
    data[id] = temp
    refresh()

def list():
    for idx, item in data.items():
        print(idx, sep=' - ')
        print(', '.join(item))

def list_status(status):
    for idx, item in data.items():
        if item[1] == status:
            print(idx)
            print(', '.join(item))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', type=add, help='add task, type any task')
    parser.add_argument('--update', nargs='+', help='update task, type any task')
    parser.add_argument('-d', '--delete', nargs=1, type=int, help='delete task, type id of task')
    parser.add_argument('--mark-in-progress', type=int, nargs=1, help='mark task in progress, type id of task')
    parser.add_argument('--mark-done', type=int, nargs=1, help='mark task in done, type id of task')
    parser.add_argument('--list', nargs='?', choices=['todo', 'in-progress', 'done'], help='type status of task')
    args = parser.parse_args()
    if args.update:
        update(args.update[0], args.update[1])
    elif args.delete:
        delete(args.delete[0])
    if args.mark_in_progress:
        mark_in_progress(args.mark_in_progress[0])
    elif args.mark_done:
        mark_done(args.mark_done[0])
    if args.list:
        if list_status(args.list) is None:
            print('Tasks is empty')
        list_status(args.list)
    elif args.list is None:
        list()