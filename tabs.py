import tkinter as tk
from tkinter import ttk

class TabApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tab App")

        self.tabControl = ttk.Notebook(self)

        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text="Tab 1")
        self.tabControl.add(self.tab2, text="Tab 2")
        self.tabControl.add(self.tab3, text="Tab 3")

        self.tabControl.pack(expand=1, fill="both")

        self.create_tab1_view()
        self.create_tab2_view()
        self.create_tab3_view()

    def create_tab1_view(self):
        canvas = tk.Canvas(self.tab1, bg="white", width=300, height=200)
        canvas.pack()

        canvas.create_rectangle(50, 50, 250, 150, fill="blue")
        canvas.create_text(150, 100, text="This is Tab 1")

    def create_tab2_view(self):
        canvas = tk.Canvas(self.tab2, bg="white", width=300, height=200)
        canvas.pack()

        canvas.create_oval(50, 50, 250, 150, fill="red")
        canvas.create_text(150, 100, text="This is Tab 2")

    def create_tab3_view(self):
        canvas = tk.Canvas(self.tab3, bg="white", width=300, height=200)
        canvas.pack()

        canvas.create_polygon(50, 150, 150, 50, 250, 150, fill="green")
        canvas.create_text(150, 100, text="This is Tab 3")

if __name__ == "__main__":
    app = TabApp()
    app.mainloop()
