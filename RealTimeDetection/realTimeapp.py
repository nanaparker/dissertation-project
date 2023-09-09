import os
import win32con
import win32file
from tkinter import *
import mainFeatures as MF
from tkinter import messagebox
from PIL import ImageTk, Image


# Class for the Log In Window
class RealTime:
    def __init__(self):
        self.login = Tk()
        self.login.configure(bg="#2f3644")
        self.login.title("Comprehensive Defence System")
        self.login.iconbitmap("img/shield.ico")
        self.login.geometry("1024x720")
        self.login.resizable(False, False)


    def setup(self):
        frame = LabelFrame(self.login, bg="#2F3644", fg="#45cd88", border=0, width=400, height=400)
        frame.place(relx=0.53, rely=0.25)

        logo = ImageTk.PhotoImage(Image.open("img/login.png"))
        logo_label = Label(self.login, image=logo, bg="#2f3644", pady=20).place(x=50, rely=0.25)

        Label(frame, text="Real Time Detection", bg="#2f3644", fg="#45cd88", 
              font=('Helvetica', 23)).place(relx=0.15, rely=0.38)

        Button(frame, padx=39, pady=15, border=0, text="PROTECT", bg="#45cd88", fg="#2f3644", cursor='hand2',
            font=('Helvetica', 11), command=lambda: self.rtd(),activebackground="#232833",
            activeforeground="#45cd88").place(relx=0.3, rely=0.72)

        self.login.mainloop()


    def logged(self):
        e_val = self.email_input.get()
        p_val = self.pswd_input.get()

        if e_val == " " or p_val == " ":
            messagebox.showerror("Invalid", "Fill in Username/Password")
        else:
            sql = MF.mySQL('10.0.11.149')
            response = sql.login(e_val, p_val)
            if response[0] == 1:
                self.email_input.delete(0, 'end')
                self.pswd_input.delete(0, 'end')
                user, set1, set2, set3 = sql.settingsRetrieval(response[1])

            else:
                messagebox.showerror("Invalid", "Invalid Username/Password")



    def rtd(self): 

        usernameUp = os.environ.get('USERNAME').upper().split(" ")
        username = os.environ.get('USERNAME')

        ACTIONS = {
            1 : "Created",
            2 : "Deleted",
            3 : "Updated",
            4 : "Renamed from something",
            5 : "Renamed to something"
        }

        FILE_LIST_DIRECTORY = 0x0001

        path_to_watch = "C:\\"
        hDir = win32file.CreateFile (
            path_to_watch,
            FILE_LIST_DIRECTORY,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
        )

        while 1:
        
            results = win32file.ReadDirectoryChangesW (
            hDir,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None
            )

            paths = [] 
        
            for action, file in results:
                paths.append(os.path.join (path_to_watch, file))
                
                if paths[0][0:32] == "C:\\Users\\{}\\AppData\\".format(username):paths.clear()
                elif paths[0][0:18] == "C:\\Users\\{}~1\\".format(usernameUp[0]):paths.clear()
                elif paths[0][0:20] == "C:\\Windows\\Prefetch\\":paths.clear()
                elif paths[0][0:15] == "C:\\Windows\\Temp":paths.clear()
                elif paths[0][0:15] == "C:\\$Recycle.Bin":paths.clear()
                elif paths[0][0:14] == "C:\\ProgramData":paths.clear()
                elif paths[0][0:23] == "C:\\Windows\\ServiceState":paths.clear()
                elif paths[0][0:15] == "C:\\Windows\\Logs":paths.clear()
                elif paths[0][0:26] == "C:\\Windows\\ServiceProfiles":paths.clear()
                elif paths[0][0:19] == "C:\\Windows\\System32":paths.clear()
                elif paths[0][0:28] == "C:\\Program Files\\CUAssistant":paths.clear()
                elif paths[0][0:23] == "C:\\Windows\\bootstat.dat":paths.clear()

                try:
                    av = MF.AV()
                    result = av.malwareChecker(paths[0])
                    if result != 0:
                        print(result)
                        messagebox.showerror("Error", result)
                except:pass
                paths.clear()

rt = RealTime()
rt.setup()
# rt.rtd()