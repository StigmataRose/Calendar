import tkinter as tk
import random

class Task:
    def __init__(self, name):
        self.name = name

class TaskBox:
    def __init__(self, root):
        self.root = root
        root.title("TaskBox")
        self.tasks = []
        
        # Determine the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
  
        # Calculate the desired window size (e.g., 80% of screen width and height)
        window_width = int(screen_width * 0.2)
        window_height = int(screen_height * 0.8)
        
        # Calculate window position to center it
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.bounds = [0, 0, window_width, window_height]
        bounds = self.bounds
        # Set the window geometry
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Scrollbar
        scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_list = tk.Listbox(self.canvas, yscrollcommand=scrollbar.set, font=("Hepatica", 12))
        self.task_list.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_window((0, 0), window=self.task_list, anchor="nw")


        self.canvas = tk.Canvas(root, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind events for resizing
        self.canvas.bind("<Configure>", self.onResize)

        # Column 1
        self.plus_button = tk.Button(root, text="+", command=self.add_task, 
                               font=("Hepatica", 14), highlightbackground='black')
        self.plus_button.place(x=(bounds[2] * 0.25), y=(bounds[3]*0.05), width=bounds[2]*0.5)    

        

    def onResize(self, event):
        # Update box size to fill frame
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        self.bounds = [0, 0, window_width, window_height]
        self.plus_button.place(x=(self.bounds[2] * 0.25), y=(self.bounds[3]*0.05), width=self.bounds[2]*0.5)  


    def create_widgets(self):
        pass

    def add_task(self):
        task_name = "Task"
        print(len(self.tasks))
        task = Task(task_name)
        self.tasks.append(task)
        # You may want to implement the logic to display the task on the canvas here

    def get_index(self, task):
        return self.tasks.index(task)

    def move_task(self, task, new_index):
        index = self.get_index(task)
        if index != -1:
            self.tasks.pop(index)
            self.tasks.insert(new_index, task)

def main():
    root = tk.Tk()
    app = TaskBox(root)
    root.mainloop()

if __name__ == "__main__":
    main()
