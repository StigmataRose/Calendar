import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        root.title("Calendar Manager")
        self.boxes = []
        # Determine the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
  
        # Calculate the desired window size (e.g., 80% of screen width and height)
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        
        # Calculate window position to center it
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window geometry
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.canvas = tk.Canvas(root, bg="lightgray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind events for resizing
        self.canvas.bind("<Configure>", self.onResize)
        # Get the current date

        # Initialize the rectangle

        self.bounds = [0, 0, window_width, window_height]
        inner_x = 50
        inner_y = 50
 
        inner_width = window_width - 100
        inner_height = window_height - 100
        color = "white"
        outline_color = "black"
        # add box
        self.background = self.canvas.create_rectangle(inner_x, inner_y, inner_width + inner_x, inner_height + inner_y, outline=outline_color, fill=color, tags="box")

        self.selected_month = datetime.now().month - 1  # Get current month (0-based index)
        current_date = datetime.now()
        self.selected_year = current_date.year 
        current_month = current_date.month
         
        self.months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        
        # Calculate cell dimensions
        top_offset = 20
        inner_offset_y = inner_y + top_offset
        inner_offset_height = inner_height - top_offset
        cell_width = inner_width / 7
        cell_height = inner_height / 6
        half_cell = cell_width / 2
        quarter_cell = half_cell / 2

        column_y = 20
        # Column 1
        self.btn_left_1 = tk.Button(root, text="<<<", command=self.prevFunction, 
                               font=("Hepatica", 14), highlightbackground='black')

        self.btn_left_1.place(x= inner_x, y=column_y, width=quarter_cell)

        # Column 2
        self.btn_middle_2 = tk.Button(root, text=f"{self.months[self.selected_month]} {self.selected_year}",command=self.prevFunction, 
                               font=("Hepatica", 14), highlightbackground='black')
        self.btn_middle_2.place(x= 1 + inner_x + quarter_cell, y=column_y, width=cell_width-2)

        # Column 3
        self.btn_right_3 = tk.Button(root, text=">>>", command=self.nextFunction, font=("Hepatica", 14), highlightbackground='black')
        self.btn_right_3.place(x=inner_x + quarter_cell + cell_width, y=column_y, width= quarter_cell)

        self.day_titles = []
        self.day_title_box = []
        self.vertical_lines = []
        self.horizontal_lines = []

        # Day Box
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        for i in range(7):
            x = inner_x + (i + 0.5) * cell_width
            y = inner_y
            self.day_titles.append(self.canvas.create_text(x, y + 10, text=days[i], font=("Hepatica", 12), fill="black"))
            bbox = (inner_x + (i * cell_width), y, inner_x + (i * cell_width) + cell_width, inner_y + top_offset)
            self.day_title_box.append(self.canvas.create_rectangle(bbox, outline="black"))
            
            
        # Draw vertical grid lines
        for i in range(1, 7):
            x = inner_x + i * cell_width
            self.vertical_lines.append(self.canvas.create_line(x, inner_offset_y, x, inner_offset_y + inner_offset_height, fill=outline_color))

        # Draw horizontal grid lines
        for i in range(1, 6):
            y = inner_y + i * cell_height
            self.horizontal_lines.append(self.canvas.create_line(inner_x, y, inner_x + inner_width, y, fill=outline_color))
            

    def onResize(self, event):
        # Update box size to fill frame
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        self.bounds = [0, 0, window_width, window_height]
        inner_x = 50
        inner_y = 50
        inner_width = window_width - 100
        inner_height = window_height - 100
        self.canvas.coords(self.background, inner_x, inner_y, inner_x + inner_width, inner_y + inner_height)
    
        #  Redraw Cells
        top_offset = 20
        column_y = 20
        inner_offset_y = inner_y + top_offset
        inner_offset_height = inner_height - top_offset
        cell_width = inner_width / 7
        cell_height = inner_height / 6
        half_cell = cell_width / 2
        quarter_cell = half_cell / 2
        # Update button dimensions
        self.btn_left_1.place_configure(x=inner_x, y=column_y, width=quarter_cell)
        self.btn_middle_2.place_configure(x=1 + inner_x + quarter_cell, y=column_y, width=cell_width-2)
        self.btn_right_3.place_configure(x=inner_x + quarter_cell + cell_width, y=column_y, width=quarter_cell)
        
        # Redraw day boxes
        cell_width = (window_width - 100) / 7
        for i in range(7):
            x = inner_x + (i + 0.5) * cell_width
            y = inner_y
            self.canvas.coords(self.day_title_box[i], inner_x + (i * cell_width), y, inner_x + (i * cell_width) + cell_width, inner_y + top_offset)
            self.canvas.coords(self.day_titles[i],x,y+10)
           
        # Redraw vertical grid lines
        for i in range(1, 7):
            x = inner_x + i * cell_width
            self.canvas.coords(self.vertical_lines[i-1], x, 50, x, window_height - 50)
        
        # Redraw horizontal grid lines
        cell_height = (window_height - 100) / 6
        for i in range(1, 6):
            y = inner_y + i * cell_height
            self.canvas.coords(self.horizontal_lines[i-1], 50, y, window_width - 50, y)

    def nextFunction(self):
        if self.selected_month == 11:  # December
            self.selected_month = 0  # Roll over to January
            self.selected_year += 1  # Increment the year
        else:
            self.selected_month += 1

        self.btn_middle_2.config(text=f"{self.months[self.selected_month]} {self.selected_year}")
        print("Next Month:", self.months[self.selected_month], self.selected_year)

    def prevFunction(self):
        if self.selected_month == 0:  # January
            self.selected_month = 11  # Roll over to December
            self.selected_year -= 1  # Decrement the year
        else:
            self.selected_month -= 1

        self.btn_middle_2.config(text=f"{self.months[self.selected_month]} {self.selected_year}")
        print("Previous Month:", self.months[self.selected_month], self.selected_year)

    def displayCalendar():
        print("display")



def main():
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
