import tkinter as tk
from tkinter import ttk, colorchooser, messagebox,simpledialog
import random

def create_name_window():
    # Create a Tkinter dialogue box
    dialog = tk.Toplevel(root)

    # StringVar to store the entered text
    entered_text_var = tk.StringVar()
    
    # Add a text entry field
    entry_field = tk.Entry(dialog, textvariable=entered_text_var)
    entry_field.pack()

    def ok_button_pressed():
        entered_text = entered_text_var.get()
        dialog.destroy()
        return entered_text

    # Function to execute when "Cancel" button is pressed
    def cancel_button_pressed():
        dialog.destroy()
        return ""

    button1 = tk.Button(dialog, text="Ok", command=ok_button_pressed)
    button1.pack(padx=5, pady=5, side=tk.LEFT)

    button2 = tk.Button(dialog, text="Cancel", command=cancel_button_pressed)
    button2.pack(padx=5, pady=5, side=tk.LEFT)

    # Make the window blocking
    dialog.wait_window()

    # Return the entered text or an empty string upon closing
    return entered_text_var.get()


def open_box_dialog(box):
    dialog = tk.Toplevel(root)
    dialog.title(box.title_text_center)

    label = tk.Label(dialog, text="Enter text:")
    label.pack(padx=10, pady=10)

    entry = tk.Entry(dialog)
    entry.text = box.title_text_center
    entry.pack(padx=10, pady=5)

    def button1_clicked():
        print("Button 1 clicked")
        new_text = entry.get()
        box.canvas.itemconfig(box.title_text_center, text=new_text)

    def button2_clicked():
        print("Button 2 clicked")
        # Your logic for button 2

    def button3_clicked():
        print("Button 3 clicked")
        # Your logic for button 3

    def button4_clicked():
        print("Button 4 clicked")
        # Your logic for button 3

    def button5_clicked():
        print("Button 5 clicked")
        dialog.destroy()
        # Your logic for button 3

    button1 = tk.Button(dialog, text="Submit", command=button1_clicked)
    button1.pack(padx=5, pady=5, side=tk.LEFT)

    button2 = tk.Button(dialog, text="Background", command=button2_clicked)
    button2.pack(padx=5, pady=5, side=tk.LEFT)

    button3 = tk.Button(dialog, text="Text", command=button3_clicked)
    button3.pack(padx=5, pady=5, side=tk.LEFT)

    button4 = tk.Button(dialog, text="OK", command=button4_clicked)
    button4.pack(padx=5, pady=5, side=tk.LEFT)

    button5 = tk.Button(dialog, text="Cancel", command=button5_clicked)
    button5.pack(padx=5, pady=5, side=tk.LEFT)

def show_dialog(event, boxes, canvas):
    
    x = event.x
    y = event.y
    print(boxes)
    # Check if the double click event occurred on any box
    for box in boxes:
        box_coords = canvas.coords(box.rect)
        print(box_coords)
        if x > box_coords[0] and x < box_coords[2] and y > box_coords[1] and y < box_coords[3]:
            # Double click occurred on this box
            print("Double click on box!")
            open_box_dialog(box)
            return

    dialog = tk.Toplevel(root)
    dialog.title("Add Box")
    
    label = tk.Label(dialog, text="What would you like to do?")
    label.pack(padx=10, pady=10)
    
    add_button = tk.Button(dialog, text="Add", command=lambda: add_action(event, boxes, canvas, dialog))
    add_button.pack(pady=5)

def add_action(event, boxes, canvas, dialog):
    # Execute commands for adding
    # For demonstration, let's print the event and boxes
    add_new_box(event, boxes,canvas)
    dialog.destroy()


def edit_action():
    # Execute commands for editing
    messagebox.showinfo("Edit", "Executing commands for editing")

def cancel_action():
    # Execute commands for canceling
    # messagebox.showinfo("Cancel", "Executing commands for canceling")
    dialog.destroy()

class ResizableBox:
    def __init__(self, canvas, x1, y1, x2, y2, color, color2, box_name):
        self.canvas = canvas
        self.color = color
        self.rect = canvas.create_rectangle(x1, y1, x2, y2, outline=color, fill=color, tags="box")
        self.handle = canvas.create_oval(x2-5, y2-5, x2+5, y2+5, outline=color, fill=color, tags="handle")

        self._drag_data = {"x": 0, "y": 0, "item": None}
        title = box_name

        # Calculate dimensions
        self.width = abs(x2 - x1)
        self.height = abs(y2 - y1)

        # Calculate midpoint of the rectangle
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2

        # Create the text centered within the rectangle
        self.title_text_center = canvas.create_text(
            mid_x, mid_y, 
            text=title, 
            fill=color2, 
            font=('Helvetica', '12', 'bold'),
            tags="title"
        )
        
        canvas.tag_bind(self.rect, "<ButtonPress-1>", self.on_click)
        canvas.tag_bind(self.rect, "<B1-Motion>", self.on_drag)
        canvas.tag_bind(self.handle, "<ButtonPress-1>", self.on_handle_click)
        canvas.tag_bind(self.handle, "<B1-Motion>", self.on_handle_drag)

    def on_click(self, event):
        self._drag_data["item"] = self.rect
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.canvas.move(self.rect, dx, dy)
        self.canvas.move(self.handle, dx, dy)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        
        # Calculate the new coordinates for centering the text
        rect_coords = self.canvas.coords(self.rect)
        mid_x = (rect_coords[0] + rect_coords[2]) / 2
        mid_y = (rect_coords[1] + rect_coords[3]) / 2
    
        # Move the center text to new coordinates
        self.canvas.coords(self.title_text_center, mid_x, mid_y)

    def on_handle_click(self, event):
        self._drag_data["item"] = self.handle
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_handle_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        self.canvas.coords(self.rect, x1, y1, x2+dx, y2+dy)
        self.canvas.coords(self.handle, x2+dx-5, y2+dy-5, x2+dx+5, y2+dy+5)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        # Calculate the new coordinates for centering the text
        rect_coords = self.canvas.coords(self.rect)
        mid_x = (rect_coords[0] + rect_coords[2]) / 2
        mid_y = (rect_coords[1] + rect_coords[3]) / 2
    
        # Move the center text to new coordinates
        self.canvas.coords(self.title_text_center, mid_x, mid_y)

# Function to add a new box
def add_new_box(event, boxes, canvas):
    x, y = event.x, event.y
    size_x = 120  # Size of the new box
    size_y = 40
    box_name = create_name_window()
    
    color = colorchooser.askcolor()[1]
    color2 = colorchooser.askcolor()[1]
    boxes.append(ResizableBox(canvas, x, y, x + size_x, y + size_y, color, color2, box_name))

root = tk.Tk()
root.title("Resizable Colored Boxes")
root.geometry("800x600")

canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

boxes = []

# Bind double-click event to the canvas using lambda
canvas.bind("<Double-1>", lambda event: show_dialog(event, boxes, canvas))


root.mainloop()
