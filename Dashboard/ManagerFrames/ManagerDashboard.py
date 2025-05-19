import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Database.DatabaseInstance import db_manager

class ManagerDashboardFrame(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        # ye confusing
        self.app = app
        self.master = master
        self.configure(bg="#f8f9fa")

        self.grid_columnconfigure(0, weight=1, uniform="equal")
        self.grid_columnconfigure(1, weight=1, uniform="equal")
        self.grid_columnconfigure(2, weight=1, uniform="equal")

        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

        self.create_dashboard()

    def create_dashboard(self):
        # === Create Frames ===
        # First column - Pie Chart + Button
        self.frame1_wrapper = self.create_bordered_frame(self)
        self.frame1_wrapper.grid(row=0, column=0, padx=10, pady=50, sticky="nsew")

        # Second column - Pie Chart + Button
        frame2_wrapper = self.create_bordered_frame(self)
        frame2_wrapper.grid(row=0, column=1, padx=10, pady=50, sticky="nsew")

        # Third column - Pie Chart + Button
        frame3_wrapper = self.create_bordered_frame(self)
        frame3_wrapper.grid(row=0, column=2, padx=10, pady=50, sticky="nsew")

        # === Content for Frame1 (Top Row) ===
        self.create_content_for_frame(self.frame1_wrapper, "Approve Car Requests", "Go to Car Approval", "CarRequest")

        # === Content for Frame2 (Top Row) ===
        self.create_content_for_frame(frame2_wrapper, "Pending Service Approvals", "Go to Service Approval", "ServiceRequest")

        # === Content for Frame3 (Top Row) ===
        self.create_content_for_frame(frame3_wrapper, "Car Maintenance", "Go to Car Deletion Approval", "Maintenance")

    def create_bordered_frame(self, parent):
        frame_wrapper = tk.Frame(parent, bd=2, relief="groove", bg="white")
        
        frame1 = tk.Frame(frame_wrapper, bg="#ecf0f1")
        frame1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        frame1_content = tk.Frame(frame_wrapper, bg="#bdc3c7")
        frame1_content.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        frame_wrapper.grid_rowconfigure(0, weight=3)
        frame_wrapper.grid_rowconfigure(1, weight=1)
        frame_wrapper.grid_columnconfigure(0, weight=1)

        return frame_wrapper

    def create_content_for_frame(self, frame_wrapper, label_text, button_text, type_of_data):
        frame1 = frame_wrapper.winfo_children()[0]
        frame1_content = frame_wrapper.winfo_children()[1]

        tk.Label(frame1, text=label_text, font=("Helvetica", 16, "bold"), bg="#f0f4f8", fg="#333").pack(pady=10)
        
        if (type_of_data == "CarRequest"):
            self.car_approval_chart(frame1)
            button = tk.Button(frame1_content, text=button_text, font=("Segoe UI", 14), fg="white", bg="#00998F", bd=0, 
                               command=lambda: self.app.menu.change_frame("Add Cars", "AddCarRequest"))
            button.pack(fill="both", expand=True)

        elif (type_of_data == "ServiceRequest"):
            self.service_approval_chart(frame1)
            button = tk.Button(frame1_content, text=button_text, font=("Segoe UI", 14), fg="white", bg="#00998F", bd=0, 
                               command=lambda: self.app.menu.change_frame("Create Service", "AddServiceRequest"))
            button.pack(fill="both", expand=True)

        elif (type_of_data == "Maintenance"):
            self.car_maintenance_chart(frame1)
            button = tk.Button(frame1_content, text=button_text, font=("Segoe UI", 14), fg="white", bg="#00998F", bd=0, 
                               command=lambda: self.app.menu.change_frame("Car Maintenance", "CarMaintenance"))
            button.pack(fill="both", expand=True)
        else: # Useless ni pero just incase
            self.create_pie_chart(frame1)
        

    def car_maintenance_chart(self, parent_frame):
         # Data for the pie chart
        labels = ['On Maintenance', 'Available'] 
        sizes = [
            db_manager.Get.get_car_count_by_status(cursor=db_manager.cursor, status="Maintenance"),
            db_manager.Get.get_car_count_by_status(cursor=db_manager.cursor,  status="Available"),
        ]
        
        # Adjusted colors to match the two categories
        colors = ['#00b3a6', '#007c6e']
        
        # Adjusted explode values for each category
        explode = (0.1, 0)  # 'Available' slice will be exploded (highlighted)
        
        # Function to show absolute numbers instead of percentages
        def format_number(pct):
            total = sum(sizes)
            val = int(round(pct / 100.0 * total))  # Round the value to get absolute numbers
            return f'{val}'

        # Create the pie chart
        fig, ax = plt.subplots(figsize=(6, 4))  # Adjusted size for better readability
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct=format_number, shadow=True, startangle=75)
        
        ax.axis('equal')  # Equal aspect ratio for a circle to ensure it stays round

        # Create the canvas for the pie chart
        chart_canvas = FigureCanvasTkAgg(fig, parent_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    def service_approval_chart(self, parent_frame):
        # Data for the pie chart
        labels = ['Available', 'Pending'] 
        sizes = [
            db_manager.Get.get_service_count_by_status(cursor=db_manager.cursor, status="Available"),
            db_manager.Get.get_service_count_by_status(cursor=db_manager.cursor, status="Pending"),
        ]
        
        # Adjusted colors to match the two categories
        colors = ['#00b3a6', '#007c6e']
        
        # Adjusted explode values for each category
        explode = (0.1, 0)  # 'Available' slice will be exploded (highlighted)
        
        # Function to show absolute numbers instead of percentages
        def format_number(pct):
            total = sum(sizes)
            val = int(round(pct / 100.0 * total))  # Round the value to get absolute numbers
            return f'{val}'

        # Create the pie chart
        fig, ax = plt.subplots(figsize=(6, 4))  # Adjusted size for better readability
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct=format_number, shadow=True, startangle=75)
        
        ax.axis('equal')  # Equal aspect ratio for a circle to ensure it stays round

        # Create the canvas for the pie chart
        chart_canvas = FigureCanvasTkAgg(fig, parent_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_pie_chart(self, parent_frame):
        # Data for the pie chart
        labels = ['Approved', 'Pending']
        sizes = [70, 30]
        colors = ['#00b3a6', '#007c6e']
        explode = (0.1, 0)

        # Function to show absolute numbers instead of percentages
        def format_number(pct):
            total = sum(sizes)
            val = int(round(pct / 100.0 * total))
            return f'{val}'

        # Create the pie chart
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
               autopct=format_number, shadow=True, startangle=75)

        ax.axis('equal')  # Equal aspect ratio for a circle

        # Create the canvas for the pie chart
        chart_canvas = FigureCanvasTkAgg(fig, parent_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    def car_approval_chart(self, parent_frame):
         # Data for the pie chart
        labels = ['Approved', 'Pending'] 
        sizes = [
            db_manager.Get.get_car_count_by_status(cursor=db_manager.cursor, status="Available"),
            db_manager.Get.get_car_count_by_status(cursor=db_manager.cursor, status="Pending"),
        ]
        
        # Adjusted colors to match the two categories
        colors = ['#00b3a6', '#007c6e']
        
        # Adjusted explode values for each category
        explode = (0.1, 0)  # 'Available' slice will be exploded (highlighted)
        
        # Function to show absolute numbers instead of percentages
        def format_number(pct):
            total = sum(sizes)
            val = int(round(pct / 100.0 * total))  # Round the value to get absolute numbers
            return f'{val}'

        # Create the pie chart
        fig, ax = plt.subplots(figsize=(6, 4))  # Adjusted size for better readability
        ax.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct=format_number, shadow=True, startangle=75)
        
        ax.axis('equal')  # Equal aspect ratio for a circle to ensure it stays round

        # Create the canvas for the pie chart
        chart_canvas = FigureCanvasTkAgg(fig, parent_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True)


    def refresh(self):
        # Destroy all widgets in the frame
        for widget in self.winfo_children():
            widget.destroy()

        # Recreate the dashboard
        self.create_dashboard()
