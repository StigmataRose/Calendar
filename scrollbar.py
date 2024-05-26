import tkinter as tk
from tkinter import simpledialog  # Import simpledialog module

class DragDropListbox(tk.Listbox):
    def __init__(self, master, **kw):
        kw['selectmode'] = tk.SINGLE
        tk.Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i

class ScrollBardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scroll Bard")
        self.root.geometry("600x400")

        # Frame for listbox and buttons
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas
        self.canvas = tk.Canvas(self.main_frame, bg="gray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.place(x=0, y=0, height=300, width=20)  # Adjust x, y, height, and width as needed


        # Listbox
        self.task_list = DragDropListbox(self.canvas, yscrollcommand=scrollbar.set, font=("Hepatica", 12))
        for i in range(1):
            self.task_list.insert(tk.END, f"Item {i+1}")
        self.task_list.pack(fill=tk.BOTH, expand=True)
        
        # Double click event to edit item name
        self.task_list.bind("<Double-1>", self.edit_item_name)

        # Configure canvas to hold listbox
        self.canvas.create_window((250, 250), window=self.task_list, anchor="center")

        # Configure canvas scrolling region
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Buttons and entry fields
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add Item", command=self.add_item)
        self.add_button.grid(row=0, column=0, padx=10)

        self.remove_button = tk.Button(self.button_frame, text="Remove Item", command=self.remove_item)
        self.remove_button.grid(row=0, column=1, padx=10)

        self.edit_entry = tk.Entry(self.button_frame, width=30)
        self.edit_entry.grid(row=0, column=2, padx=10)

        self.edit_button = tk.Button(self.button_frame, text="Edit Selected", command=self.edit_selected)
        self.edit_button.grid(row=0, column=3, padx=10)

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def edit_item_name(self, event):
        index = self.task_list.curselection()[0]
        current_name = self.task_list.get(index)
        new_name = simpledialog.askstring("Edit Item Name", "Enter new name:", initialvalue=current_name)
        if new_name:
            self.task_list.delete(index)
            self.task_list.insert(index, new_name)

    def add_item(self):
        item_name = self.edit_entry.get()
        if item_name:
            self.task_list.insert(tk.END, item_name)
            self.edit_entry.delete(0, tk.END)

    def remove_item(self):
        try:
            index = self.task_list.curselection()[0]
            self.task_list.delete(index)
        except IndexError:
            pass

    def edit_selected(self):
        try:
            index = self.task_list.curselection()[0]
            current_name = self.task_list.get(index)
            new_name = self.edit_entry.get()
            if new_name:
                self.task_list.delete(index)
                self.task_list.insert(index, new_name)
                self.edit_entry.delete(0, tk.END)
        except IndexError:
            pass

root = tk.Tk()
app = ScrollBardApp(root)
root.mainloop()
