import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import messagebox

class TodoManager:

    def __init__(self):
        self.connection = self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="pass",  # Replace with your actual password
                database="todo"
            )
            if connection.is_connected():
                print("Connected to MySQL Database")
                return connection

        except Error as e:
            print(f"Error: {e}")
            return None

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task_name VARCHAR(255) NOT NULL
        )
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
            print("Table 'tasks' created successfully")

        except Error as e:
            print(f"Error: {e}")

    def add_task(self):
        entry_text = entry.get()
        if not entry_text:
            messagebox.showwarning("Warning", "Please enter a task before adding.")
            return

        add_task_query = "INSERT INTO tasks (task_name) VALUES (%s)"
        task_data = (entry_text,)

        try:
            cursor = self.connection.cursor()
            cursor.execute(add_task_query, task_data)
            self.connection.commit()
            cursor.fetchall()  # Fetch the result to clear the unread result
            messagebox.showinfo("Success", f'Task "{entry_text}" added successfully')

        except Error as e:
            print(f"Error: {e}")

    def remove_task(self):
        entry1_text = entry1.get()
        if not entry1_text:
            messagebox.showwarning("Warning", "Please enter a task before removing.")
            return

        check_task_query = "SELECT * FROM tasks WHERE task_name = %s"
        task_data = (entry1_text,)

        try:
            cursor = self.connection.cursor()
            cursor.execute(check_task_query, task_data)
            existing_task = cursor.fetchone()

            if existing_task:
                remove_task_query = "DELETE FROM tasks WHERE task_name = %s"
                cursor.execute(remove_task_query, task_data)
                self.connection.commit()
                messagebox.showinfo("Success", f'Task "{entry1_text}" removed successfully')
            else:
                messagebox.showwarning("Warning", f"Task '{entry1_text}' not found.")

        except Error as e:
            print(f"Error: {e}")

    def show_tasks(self):
        show_tasks_query = "SELECT * FROM tasks"

        try:
            cursor = self.connection.cursor()
            cursor.execute(show_tasks_query)
            tasks = cursor.fetchall()

            if tasks:
                task_info = "\n".join([f"{task[0]}. {task[1]}" for task in tasks])
                messagebox.showinfo("Tasks", task_info)
            else:
                messagebox.showwarning("Warning", "No Tasks Found.")

        except Error as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    todo_manager = TodoManager()

    window = Tk()
    window.geometry("450x450")
    window.title("To-Do List")

    # Entry for adding tasks
    entry = Entry(window, font=("Arial", 16)).grid(row=0, column=0)

    # Entry for removing tasks
    entry1 = Entry(window, font=("Arial", 16)).grid(row=1, column=0)

    # Button for adding tasks
    button = Button(window,
                    text="Add Task",
                    command=todo_manager.add_task,
                    font=("Arial", 12),
                    fg="black",
                    bg="white",
                    activeforeground="black",
                    activebackground="white",
                    state=ACTIVE).grid(row=0, column=1)

    # Button for removing tasks
    button2 = Button(window,
                     text="Remove Task",
                     command=todo_manager.remove_task,
                     font=("Arial", 12),
                     fg="black",
                     bg="white",
                     activeforeground="black",
                     activebackground="white",
                     state=ACTIVE).grid(row=1, column=1)

    # Button for showing tasks
    button3 = Button(window,
                     text="Show Tasks",
                     command=todo_manager.show_tasks,
                     font=("Arial", 12),
                     fg="black",
                     bg="white",
                     activeforeground="black",
                     activebackground="white",
                     state=ACTIVE).grid(row=2, column=1)

    window.mainloop()

