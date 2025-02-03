import tkinter as tk
from tkinter import messagebox, ttk
import requests # type: ignore

API_BASE_URL = "http://127.0.0.1:8000/api/tasks/"  

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("500x500")

        self.task_list = []
        
        # UI Elements
        self.task_label = tk.Label(root, text="Task Title:")
        self.task_label.pack()

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack()

        self.category_label = tk.Label(root, text="Category:")
        self.category_label.pack()

        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(root, textvariable=self.category_var, values=["Work", "Personal", "Other"])
        self.category_dropdown.pack()

        self.status_label = tk.Label(root, text="Status:")
        self.status_label.pack()

        self.status_var = tk.StringVar()
        self.status_dropdown = ttk.Combobox(root, textvariable=self.status_var, values=["Pending", "Completed"])
        self.status_dropdown.pack()

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.task_listbox = tk.Listbox(root, width=50, height=15)
        self.task_listbox.pack()
        self.task_listbox.bind("<Double-Button-1>", self.edit_task)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        self.filter_var = tk.StringVar()
        self.filter_dropdown = ttk.Combobox(root, textvariable=self.filter_var, values=["All", "Pending", "Completed"], state="readonly")
        self.filter_dropdown.pack()
        self.filter_dropdown.set("All")
        self.filter_dropdown.bind("<<ComboboxSelected>>", self.filter_tasks)

        self.load_tasks()

    def load_tasks(self):
        """Fetch all tasks from the API and display them."""
        self.task_listbox.delete(0, tk.END)
        response = requests.get(API_BASE_URL)
        if response.status_code == 200:
            self.task_list = response.json()
            for task in self.task_list:
                self.task_listbox.insert(tk.END, f"{task['title']} [{task['status']}] - {task['category']}")

    def add_task(self):
        """Send a new task to the API."""
        title = self.task_entry.get()
        category = self.category_var.get()
        status = self.status_var.get()

        if not title:
            messagebox.showwarning("Warning", "Task title cannot be empty!")
            return

        data = {"title": title, "category": category, "status": status}
        response = requests.post(API_BASE_URL + "add/", json=data)

        if response.status_code == 201:
            messagebox.showinfo("Success", "Task added successfully!")
            self.load_tasks()
        else:
            messagebox.showerror("Error", "Failed to add task.")

    def edit_task(self, event):
        """Edit a selected task from the list."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.task_list[selected_index]
            
            new_title = tk.simpledialog.askstring("Edit Task", "Update task title:", initialvalue=task["title"])
            if new_title:
                data = {"title": new_title, "category": task["category"], "status": task["status"]}
                response = requests.put(f"{API_BASE_URL}update/{task['id']}/", json=data)
                
                if response.status_code == 200:
                    messagebox.showinfo("Success", "Task updated successfully!")
                    self.load_tasks()
                else:
                    messagebox.showerror("Error", "Failed to update task.")
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to edit.")

    def delete_task(self):
        """Delete a selected task."""
        try:
            selected_index = self.task_listbox.curselection()[0]
            task = self.task_list[selected_index]

            confirm = messagebox.askyesno("Confirm", f"Delete '{task['title']}'?")
            if confirm:
                response = requests.delete(f"{API_BASE_URL}delete/{task['id']}/")

                if response.status_code == 204:
                    messagebox.showinfo("Deleted", "Task deleted successfully!")
                    self.load_tasks()
                else:
                    messagebox.showerror("Error", "Failed to delete task.")
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def filter_tasks(self, event):
        """Filter tasks by status."""
        selected_status = self.filter_var.get()
        self.task_listbox.delete(0, tk.END)

        for task in self.task_list:
            if selected_status == "All" or task["status"] == selected_status:
                self.task_listbox.insert(tk.END, f"{task['title']} [{task['status']}] - {task['category']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
