import tkinter as tk
from Helper import Helper
from Database.DatabaseInstance import db_manager
from StartingFrames.Login import LoginFrame
from StartingFrames.Register import RegisterFrame
from Session.PseudoSession import Session



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Center ang gui pag I create
        self.geometry(f"400x550+{(self.winfo_screenwidth()//2)-100}+{(self.winfo_screenheight()//2)-300}")
        self.title("Vehicle Management System")
        

        self.resizable(False, False)

        # Frame holder
        self.mainFrame = tk.Frame(self)
        self.mainFrame.pack(expand=True, fill='both')

        # If new frame add lang diri
        self.frames = {
            "LoginFrame": LoginFrame(self.mainFrame, self),
            "RegisterFrame": RegisterFrame(self.mainFrame, self),
        }

        # Place all frames in mainframe but only raises the needed one
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.currentFrame = None
        self.ChangeFrame("LoginFrame")

        self.bind("<Configure>", self.AdjustFontSize)


    def ChangeFrame(self, frame_name):
        self.currentFrame = frame_name
        self.frames[frame_name].tkraise()
        self.AdjustFontSize(self) 


    def AdjustFontSize(self, event):
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        font_size = max(min(int(window_width / 20), int(window_height / 20)), 10)
        self.frames[self.currentFrame].AdjustFontSize(font_size)

    def GoToDashboard(self, email, password):
        self.CreateSession(email=email, password=password)
        self.destroy()
        Helper.after_login()
        
    
    # Create session
    def CreateSession(self, email, password):   
        Data = db_manager.Get.get_user_data(
            conn=db_manager.conn, 
            cursor=db_manager.cursor,
            email=email,
            password=password)
        
        if Data:
            Session.NewSession(
                id=Data["id"],
                name=f"{Data['first_name']} {Data['last_name']}",
                email=Data["email"],
                role=Data["role"]
            )


      

if __name__ == "__main__":
    app = App()
    app.mainloop()
    
