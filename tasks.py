import tkinter as tk
import tkinter.messagebox as msg
import json

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.tasks = self.load_tasks()

        self.task_entry = tk.Entry(root, width=50)
        self.task_list = tk.Listbox(root, width=50)
        self.task_list.bind('<Double-1>', self.complete_task)  # Bind double-click event

        self.add_button = tk.Button(root, text="Add task", command=self.add_task)
        self.complete_button = tk.Button(root, text="Complete task", command=self.complete_task)
        self.move_up_button = tk.Button(root, text="Move up", command=self.move_up)
        self.move_down_button = tk.Button(root, text="Move down", command=self.move_down)

        self.task_entry.grid(row=0, column=0, padx=10, pady=10)
        self.task_list.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
        self.add_button.grid(row=0, column=1, padx=10, pady=10)
        self.complete_button.grid(row=2, column=0, padx=10, pady=10)
        self.move_up_button.grid(row=2, column=1, padx=10, pady=10)
        self.move_down_button.grid(row=3, column=1, padx=10, pady=10)

        self.view_tasks()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f)

    def add_task(self):
        tasks = self.task_entry.get().split(',')
        for task in tasks:
            task = task.strip()  # Remove leading and trailing whitespace
            if task:
                self.tasks.append(task)
        self.task_entry.delete(0, tk.END)
        self.view_tasks()
        self.save_tasks()

    def view_tasks(self):
        self.task_list.delete(0, tk.END)
        for task in self.tasks:
            self.task_list.insert(tk.END, task)

    def complete_task(self, event=None):  # Add event parameter for double-click event
        try:
            task_index = self.task_list.curselection()[0]
            confirm = msg.askyesno("Task Manager", "Are you sure you want to complete this task?")
            if confirm:
                del self.tasks[task_index]
                self.view_tasks()
                self.save_tasks()
        except IndexError:
            msg.showinfo("Task Manager", "No task selected")

    def move_up(self):
        try:
            task_index = self.task_list.curselection()[0]
            if task_index > 0:
                self.tasks[task_index], self.tasks[task_index - 1] = self.tasks[task_index - 1], self.tasks[task_index]
                self.view_tasks()
                self.task_list.select_set(task_index - 1)
                self.save_tasks()
        except IndexError:
            msg.showinfo("Task Manager", "No task selected")

    def move_down(self):
        try:
            task_index = self.task_list.curselection()[0]
            if task_index < len(self.tasks) - 1:
                self.tasks[task_index], self.tasks[task_index + 1] = self.tasks[task_index + 1], self.tasks[task_index]
                self.view_tasks()
                self.task_list.select_set(task_index + 1)
                self.save_tasks()
        except IndexError:
            msg.showinfo("Task Manager", "No task selected")

root = tk.Tk()
root.title("Task Manager")
task_manager = TaskManager(root)
root.mainloop()