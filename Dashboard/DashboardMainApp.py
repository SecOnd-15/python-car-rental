import tkinter as tk
from Dashboard.DashboardMenu import DashboardMenu
from Session.PseudoSession import Session
import matplotlib.pyplot as plt
import sys

from Dashboard.AdminFrames.StaffManagement import StaffManagementFrame
from Dashboard.ManagerFrames.AddCarRequest import AddCarRequestFrame
from Dashboard.ManagerFrames.CarDeleteRequest import CarDeleteRequestFrame
from Dashboard.ManagerFrames.AddServiceRequest import AddServiceRequestFrame
from Dashboard.ManagerFrames.CarMaintenance import CarMaintenanceFrame
from Dashboard.ManagerFrames.ManagerDashboard import ManagerDashboardFrame

from Dashboard.AdminFrames.CarApproval import CarApprovalFrame
from Dashboard.AdminFrames.CarDeletionApproval import CarDeletionApprovalFrame
from Dashboard.AdminFrames.EditCarRentalPrice import EditCarRentalPriceFrame
from Dashboard.AdminFrames.ServiceApproval import ServiceApprovalFrame
from Dashboard.AdminFrames.Dashboard import AdminDashboardFrame
from Dashboard.AdminFrames.Report import ReportFrame

from Dashboard.StaffFrames.AddCustomer import AddCustomerFrame
from Dashboard.StaffFrames.RentCar import RentCarFrame
from Dashboard.StaffFrames.ReturnRent import ReturnRentFrame

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__() 
        self.title("Dashboard")
        self.state('zoomed')
        self.geometry(f"800x600+{(self.winfo_screenwidth()//2)-425}+{(self.winfo_screenheight()//2)-350}")

        self.header_frame = tk.Frame(self, bg="#f5f5f5", pady=20, padx=20, bd=1, relief="sunken", highlightbackground="#00998F", highlightthickness=0.5)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        welcome_label = tk.Label(self.header_frame, text=f"Welcome, {Session.session_name}!", 
                                 font=("Helvetica", 14, "bold"), bg="#f5f5f5")
        welcome_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        # User Info: ID and Role
        user_id_label = tk.Label(self.header_frame, text=f"User ID: {Session.session_id}", 
                                 font=("Helvetica", 10), bg="#f5f5f5")
        user_id_label.grid(row=1, column=0, sticky="w", padx=(0, 10))

        role_label = tk.Label(self.header_frame, text=f"Role: {Session.session_role}", 
                              font=("Helvetica", 10), bg="#f5f5f5")
        role_label.grid(row=1, column=1, sticky="w")


        

        # Dashboard Menu
        self.menu = DashboardMenu(self, app=self)
        self.menu.grid(row=1, column=0, sticky="nsew")

       
        self.mainFrame = tk.Frame(self)
        self.mainFrame.grid(row=1, column=1, sticky="nsew")

        # Frames dictionary
        self.frames = {
            "StaffManagement": StaffManagementFrame(self.mainFrame, app=self),
            "AddCarRequest": AddCarRequestFrame(self.mainFrame, app=self),
            "CarApproval": CarApprovalFrame(self.mainFrame, app=self),
            "CarDeletionRequest": CarDeleteRequestFrame(self.mainFrame, app=self),
            "CarDeletionApproval": CarDeletionApprovalFrame(self.mainFrame, app=self),
            "EditCarRentalPrice": EditCarRentalPriceFrame(self.mainFrame, app=self),
            "AddServiceRequest": AddServiceRequestFrame(self.mainFrame, app=self),
            "ServiceApproval": ServiceApprovalFrame(self.mainFrame, app=self),
            "CarMaintenance": CarMaintenanceFrame(self.mainFrame, app=self),
            "RentCar": RentCarFrame(self.mainFrame, app=self),
            "AddCustomer": AddCustomerFrame(self.mainFrame, app=self),
            "ReturnRent": ReturnRentFrame(self.mainFrame, app=self),
            "Dashboard": AdminDashboardFrame(self.mainFrame, app=self),
            "Report": ReportFrame(self.mainFrame, app=self),
            "ManagerDashboard": ManagerDashboardFrame(self.mainFrame, app=self)
        }

       
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        
        self.currentFrame = None


     
        if Session.session_role == "Admin":
            self.ChangeFrame("Report")
        elif Session.session_role == "Manager":
            self.ChangeFrame("ManagerDashboard")
        elif Session.session_role == "Staff":
            self.ChangeFrame("RentCar")

        # 10% ang menu
        self.grid_rowconfigure(0, weight=0)  
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=9)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.mainloop()


       
    # Matplot goofy ah bug remove; tanan chart kung i close ang window
    def on_closing(self):
        plt.close('all')
        

    def ChangeFrame(self, frame_name):
        """Switch between frames"""
        self.currentFrame = frame_name
        self.frames[frame_name].tkraise()
        




