import tkinter as tk
from tkinter import messagebox, colorchooser, ttk
import calendar
from datetime import datetime

class CalendarWithTasks:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar with Tasks")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.year_label = ttk.Label(root, text="Year:")
        self.year_label.grid(row=0, column=0)
        self.year_entry = ttk.Entry(root)
        self.year_entry.insert(0, self.current_year)
        self.year_entry.grid(row=0, column=1)

        self.month_label = ttk.Label(root, text="Month:")
        self.month_label.grid(row=1, column=0)
        self.month_entry = ttk.Entry(root)
        self.month_entry.insert(0, self.current_month)
        self.month_entry.grid(row=1, column=1)

        self.show_button = ttk.Button(root, text="Show Calendar", command=self.display_calendar)
        self.show_button.grid(row=2, columnspan=2)

        self.navigation_frame = ttk.Frame(root)
        self.navigation_frame.grid(row=3, columnspan=2)

        self.prev_button = ttk.Button(self.navigation_frame, text="Previous", command=self.show_previous_month)
        self.prev_button.pack(side=tk.LEFT)

        self.next_button = ttk.Button(self.navigation_frame, text="Next", command=self.show_next_month)
        self.next_button.pack(side=tk.LEFT)

        self.calendar_frame = ttk.Frame(root)
        self.calendar_frame.grid(row=4, columnspan=2)
    
        self.tasks = {}

        # Display the calendar initially
        self.display_calendar()

    def display_calendar(self):
        year = int(self.year_entry.get())
        month = int(self.month_entry.get())

        # Add a label for the month
        month_name_label = ttk.Label(self.calendar_frame, text=calendar.month_name[month] + " " + str(year))
        month_name_label.grid(row=0, column=0, columnspan=7, pady=10)

        # Add labels for the days of the week
        days_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col_num, day_label in enumerate(days_labels):
            day_label = ttk.Label(self.calendar_frame, text=day_label)
            day_label.grid(row=1, column=col_num, padx=5, pady=5)

        cal = calendar.monthcalendar(year, month)
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        for row_num, week in enumerate(cal):
            for col_num, day in enumerate(week):
                if day == 0:
                    continue
                date_str = f"{year}-{month:02d}-{day:02d}"
                day_frame = ttk.Frame(self.calendar_frame, width=100, height=100)
                day_frame.grid(row=row_num, column=col_num, padx=5, pady=5)
                day_label = ttk.Label(day_frame, text=str(day))
                day_label.pack(side=tk.TOP)
                text_entry = tk.Text(day_frame, height=3, width=10)
                text_entry.pack(side=tk.TOP)
                color_button = ttk.Button(day_frame, text="Pick Color", command=lambda date=date_str: self.pick_color(date))
                color_button.pack(side=tk.TOP)

                if date_str in self.tasks:
                    tasks = self.tasks[date_str]
                    for task in tasks:
                        task_frame = ttk.Frame(day_frame, relief="raised", borderwidth=1)
                        task_frame.pack(side=tk.TOP, pady=2, fill=tk.X)
                        task_label = ttk.Label(task_frame, text=task["text"], background=task["color"])
                        task_label.pack(side=tk.LEFT, padx=2)
                        delete_button = ttk.Button(task_frame, text="Delete", command=lambda date=date_str, task=task: self.delete_task(date, task))
                        delete_button.pack(side=tk.RIGHT)

    def pick_color(self, date):
        color = colorchooser.askcolor()[1]
        if color:
            if date in self.tasks:
                for task in self.tasks[date]:
                    task["color"] = color
            else:
                self.tasks[date] = []
            self.display_calendar()

    def add_task(self, date, text, color):
        if date in self.tasks:
            self.tasks[date].append({"text": text, "color": color})
        else:
            self.tasks[date] = [{"text": text, "color": color}]
        self.display_calendar()

    def delete_task(self, date, task):
        if date in self.tasks:
            self.tasks[date].remove(task)
            self.display_calendar()

    def show_previous_month(self):
        current_year = int(self.year_entry.get())
        current_month = int(self.month_entry.get())
        if current_month == 1:
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1
        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, current_year)
        self.month_entry.delete(0, tk.END)
        self.month_entry.insert(0, current_month)
        self.display_calendar()

    def show_next_month(self):
        current_year = int(self.year_entry.get())
        current_month = int(self.month_entry.get())
        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1
        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, current_year)
        self.month_entry.delete(0, tk.END)
        self.month_entry.insert(0, current_month)
        self.display_calendar()

def main():
    root = tk.Tk()
    calendar_app = CalendarWithTasks(root)
   
    root.mainloop()

if __name__ == "__main__":
    main()
