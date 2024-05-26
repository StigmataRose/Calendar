import tkinter as tk
from tkinter import messagebox, colorchooser

class BoxApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Box Manager")

        self.boxes_frame = tk.Frame(self.master)
        self.boxes_frame.pack(padx=10, pady=10)

        self.boxes = []
        self.selected_box = None  # To keep track of the selected box
        self.add_box()

        self.add_button = tk.Button(self.master, text="+", command=self.add_box)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.remove_button = tk.Button(self.master, text="-", command=self.remove_box)
        self.remove_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.master, text="Save", command=self.save_boxes)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_button = tk.Button(self.master, text="Load", command=self.load_boxes)
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Bind event to update selected box when focus changes
        self.master.bind('<FocusIn>', self.update_selected_box)
        self.numBoxes = 0
        self.selected_box = 0
    
    def add_box(self):
        new_box = Box(self.boxes_frame, self.master)
        self.boxes.append(new_box)
        new_box.pack(fill=tk.X, padx=5, pady=5)
    
    def remove_box(self):
        if self.selected_box:
            self.boxes.remove(self.selected_box)
            self.selected_box.destroy()
            self.selected_box = None
        else:
            messagebox.showinfo("Warning", "No box selected!")

    def save_boxes(self):
        with open("boxes.txt", "w") as f:
            for box in self.boxes:
                title = box.title_entry.get()
                color = box.bg_color
                checked = box.checkbox_var.get()
                f.write(f"{title},{color},{checked}\n")

    def load_boxes(self):
        try:
            with open("boxes.txt", "r") as f:
                for line in f:
                    title, color, checked = line.strip().split(",")
                    new_box = Box(self.boxes_frame, self.master)
                    new_box.title_entry.insert(0, title)
                    new_box.title_entry.config(bg=color)
                    new_box.checkbox_var.set(checked == 'True')
                    self.boxes.append(new_box)
                    new_box.pack(fill=tk.X, padx=5, pady=5)
        except FileNotFoundError:
            messagebox.showinfo("Warning", "No saved boxes found.")

    def update_selected_box(self, event):
        focused_widget = self.master.focus_get()
        if focused_widget in self.boxes:
            self.selected_box = focused_widget

class Box(tk.Frame):
    def __init__(self, master, app_master):
        super().__init__(master, bg="white")

        self.title = "Box"
        self.bg_color = "white"
        self.app_master = app_master
        self.boxID = 0

        self.title_entry = tk.Entry(self, bg=self.bg_color)
        self.title_entry.insert(0, self.title)
        self.title_entry.pack(side=tk.LEFT)

        self.checkbox_var = tk.BooleanVar()
        self.checkbox = tk.Checkbutton(self, variable=self.checkbox_var, bg="white")
        self.checkbox.pack(side=tk.LEFT)

        self.change_color_button = tk.Button(self, text="CC", command=self.change_color)
        self.change_color_button.pack(side=tk.LEFT)

        self.bind("<Double-Button-1>", self.change_color)

    def change_color(self, event=None):
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color
            self.title_entry.config(bg=self.bg_color)

def main():
    root = tk.Tk()
    app = BoxApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
