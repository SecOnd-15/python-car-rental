import tkinter as tk
from Session.PseudoSession import Session
import matplotlib.pyplot as plt
import sys


class DashboardMenu(tk.Frame):
    def __init__(self, master=None, app=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#D3D3D3", padx=10, pady=10)
        self.app = app
        self.buttons = []
        self.last_pressed = None
        self.need_refresh = {"RentCar", "ReturnRent", "Dashboard", "Report"}

        # self.add_button("Statistic", "Statistic")

        if Session.session_role == "Staff":
            #self.add_button("Create Request", "CreateRequest")
            self.add_button("Create Car Rent", "RentCar")
            self.add_button("Add Customer", "AddCustomer")
            self.add_button("Return Cars Rent", "ReturnRent")
            

        if Session.session_role == "Manager":
            self.add_button("Dashboard", "ManagerDashboard")
            self.add_button("Add Cars", "AddCarRequest")
            self.add_button("Delete Cars", "CarDeletionRequest")
            self.add_button("Car Maintenance", "CarMaintenance")
            #self.add_button("View Request", "ViewRequest")
            self.add_button("Create Service", "AddServiceRequest")
           

        if Session.session_role == "Admin":
            self.add_button("Dashboard Report", "Report")
            self.add_button("Dashboard", "Dashboard")
            self.add_button("User Management", "StaffManagement")
            self.add_button("Car Approval", "CarApproval")
            self.add_button("Car Deletion Approval", "CarDeletionApproval")
            self.add_button("Edit Rental Price", "EditCarRentalPrice")
            self.add_button("Service Approval", "ServiceApproval")
            
          
        self.logoutButton = tk.Button(
            self,
            text="Logout",
            command=self.logout,
            bd=0,
            relief="flat",
            font=("Arial", 12, "bold"),
            fg="#FFFFFF",
            bg="#c0392b",
            padx=10,
            pady=5
        )
        self.logoutButton.pack(side="bottom", fill="x", pady=5)

        

    def add_button(self, label, frame_name):
        btn = tk.Button(
            self,
            text=label,
            command=lambda b=label, f=frame_name: self.change_frame(b, f),
            bd=0,
            relief="flat",
            font=("Arial", 12, "bold"),
            fg="#FFFFFF",
            bg="#00998F",
            padx=10,
            pady=5
        )
        btn.pack(fill="x", pady=5)
        self.buttons.append((label, btn))

    def change_frame(self, label, frame_name):
        if self.last_pressed:
            self.last_pressed.configure(bg="#00998F", fg="#FFFFFF")

        for lbl, btn in self.buttons:
            if lbl == label:
                btn.configure(bg="#FFFFFF", fg="#00998F")
                self.last_pressed = btn
                break

        if frame_name in self.need_refresh:
            self.app.frames[frame_name].refresh()

        self.app.ChangeFrame(frame_name)

    def logout(self):
        self.app.on_closing()
        self.app.destroy()
        from main import App
        App().mainloop()

        
