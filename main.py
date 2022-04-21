import json
import datetime
import os
import shutil
import urllib.request


def search_json(key, obj):  # Функция поиска объекта по json
    run = 0
    while run < len(obj):
        if key not in obj[run]:
            obj.remove(obj[run])  # удаляет объект, если нет ключа в списке
        else:
            run += 1


def observe_title():  # Функция среза лишнего текста
    if len(tasks['title']) < 48:
        tasks['title'] = tasks['title']
    else:
        tasks['title'] = tasks['title'][0:48] + '...'


try:
    with urllib.request.urlopen('https://json.medrating.org/users') as file:
        users = json.load(file)
        print(len(users))
    
    with urllib.request.urlopen('https://json.medrating.org/todos') as file:
        todos = json.load(file)
    
    path = r'tasks'
    os.makedirs(path, exist_ok=True)  # Создание директории
    
    search_json('username', users)
    search_json('userId', todos)
    
    i = 1  # Счетчик для id
    j = 0  # Счетчик по списку
    while i < len(users) + 1:
        
        cases = [case for case in todos if case['userId'] == i]
        finished_tasks, unfinished_tasks = [], []
        sum_finished_tasks, sum_unfinished_tasks = 0, 0
        
        for tasks in cases:
            if tasks['completed']:
                observe_title()
                finished_tasks.append(tasks['title'])
                sum_finished_tasks += 1
            else:
                observe_title()
                unfinished_tasks.append(tasks['title'])
                sum_unfinished_tasks += 1
        
        now = datetime.datetime.strftime(datetime.datetime.now(), "%d.%m.%Y %H:%M")

        unfinished_tasks = '\n'.join(str(value) for value in unfinished_tasks)
        finished_tasks = '\n'.join(str(value) for value in finished_tasks)
        all_tasks = sum_finished_tasks + sum_unfinished_tasks
        
        if os.path.isfile(rf"{path}\{users[j]['username']}.txt"):
            last_md_date = os.stat(rf"{path}\{users[j]['username']}.txt").st_mtime  # Использование последней модификации файла
            result_date = datetime.datetime.fromtimestamp(last_md_date).strftime('%Y-%m-%dT%H.%M')
            shutil.copy(rf"{path}\{users[j]['username']}.txt", rf"{path}\old_{users[j]['username']}_{result_date}.txt")
        
        with open(rf"{path}\{users[j]['username']}.txt", 'w', encoding='utf-8') as file:
            if users[j]["name"] != 0:
                file.write(
                    f"Отчёт для {users[j]['username']}.\n" +
                    f"{users[j]['name']} <{users[j]['email']}> {now}\n" +
                    f"Всего задач: {all_tasks}\n\n" +
                    f"Завершенные задачи ({sum_finished_tasks}):\n" +
                    f"{finished_tasks}\n\n" +
                    f"Оставшиеся задачи ({sum_unfinished_tasks}):\n" +
                    f"{unfinished_tasks}")
        j += 1
        i += 1
except:
    raise OSError('Не удалось загрузить данные')
