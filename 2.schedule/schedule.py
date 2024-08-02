import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import datetime
import os

class Task:
    def __init__(self, name, deadline):
        self.name = name
        self.deadline = datetime.datetime.strptime(deadline, '%H:%M').time()

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("计划表")
        self.root.geometry("400x600")
        self.root.attributes("-topmost", True)
        # self.root.configure(bg='#c5e5f4')
        self.root.wm_attributes("-transparentcolor", "#c5e5f4")
        self.root.wm_attributes("-alpha", 0.9)

        self.tasks = []
        self.task_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, bg='#c5e5f4', selectbackground='purple',
                                       font=('Arial', 14), fg='white', selectforeground='black')
        self.task_listbox.pack(fill=tk.BOTH, expand=True)

        button_frame = tk.Frame(root, relief=tk.RIDGE, borderwidth=2)
        button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.add_task_button = tk.Button(button_frame, text="添加计划", command=self.add_task, bg="SystemButtonFace")
        self.add_task_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_task_button = tk.Button(button_frame, text="删除选中计划", command=self.delete_selected_tasks,
                                            bg="SystemButtonFace")
        self.delete_task_button.pack(side=tk.LEFT, padx=5, pady=5)


        self.load_tasks()
        self.update_task_list()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def add_task(self):
        task_name = simpledialog.askstring("添加计划", "请输入计划名称:")
        if task_name:
            deadline_str = simpledialog.askstring("截止时间", "请输入截止时间 (格式: HH:MM):")
            if deadline_str:
                try:
                    deadline_time = datetime.datetime.strptime(deadline_str, '%H:%M').time()
                    new_task = Task(task_name, deadline_str)
                    self.tasks.append(new_task)
                    self.update_task_list()
                except ValueError:
                    messagebox.showerror("错误", "时间格式不正确，请使用 HH:MM 格式。")

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r", encoding="utf-8") as file:
                tasks_data = json.load(file)
                self.tasks = [
                    Task(task['name'], task['deadline'])
                    for task in tasks_data
                ]

    def delete_selected_tasks(self):
        selected_indices = self.task_listbox.curselection()
        for index in reversed(selected_indices):
            del self.tasks[index]
        self.update_task_list()

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        sorted_tasks = sorted(self.tasks, key=lambda task: task.deadline)
        for task in sorted_tasks:
            self.task_listbox.insert(tk.END, f"{task.name} (截止: {task.deadline.strftime('%H:%M')})")

    def load_tasks(self):
        if os.path.exists("tasks.txt"):
            with open("tasks.txt", "r", encoding="utf-8") as file:
                tasks_data = json.load(file)
                self.tasks = [
                    Task(task['name'], task['deadline'])
                    for task in tasks_data
                ]

    def save_tasks(self):
        tasks_data = [
            {'name': task.name, 'deadline': task.deadline.strftime('%H:%M')}
            for task in self.tasks
        ]
        with open("tasks.txt", "w", encoding="utf-8") as file:
            json.dump(tasks_data, file)

    def on_closing(self):
        self.save_tasks()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
