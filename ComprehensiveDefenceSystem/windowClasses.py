import os
import time
import threading
from tkinter import *
from tkinter import ttk
from datetime import date
import mainFeatures as MF
from tkinter import messagebox
from PIL import ImageTk, Image


# Class for the Log In Window
class LoginPage:
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

        heading = Label(frame, text="Sign In", bg="#2f3644", fg="#45cd88", font=('Helvetica', 23)).place(relx=0.4, y=5)

        email_label = Label(frame, text="EMAIL", bg="#2f3644", fg="#84888f",
                            font=('Helvetica', 11)).place(relx=0, rely=0.18)
        self.email_input = Entry(frame, width=50, bg="#232833", fg="#84888f", border=0, font=('Helvetica', 14))
        self.email_input.place(relx=0, rely=0.25, height=50)

        pswd_label = Label(frame, text="PASSWORD", bg="#2f3644", fg="#84888f", font=('Helvetica', 11)).place(relx=0, rely=0.45)
        self.pswd_input = Entry(frame, show="*", width=50, bg="#232833", fg="#84888f", border=0, font=('Helvetica', 14))
        self.pswd_input.place(relx=0, rely=0.52, height=50)

        Button(frame, padx=39, pady=15, border=0, text="LOG IN", bg="#45cd88", fg="#2f3644", cursor='hand2',
            font=('Helvetica', 11), command=self.logged,activebackground="#232833",
            activeforeground="#45cd88").place(relx=0.665, rely=0.72)
        
        self.login.mainloop()

    def logged(self):
        e_val = self.email_input.get()
        p_val = self.pswd_input.get()

        if e_val == " " or p_val == " ":
            messagebox.showerror("Invalid", "Fill in Username/Password")
        else:
            sql = MF.mySQL('192.168.56.101')
            response = sql.login(e_val, p_val)
            if response[0] == 1:
                self.email_input.delete(0, 'end')
                self.pswd_input.delete(0, 'end')
                user, set1, set2, set3 = sql.settingsRetrieval(response[1])

                home = HomePage(self.login, user, set1, set2, set3)
                home.placeItems()
            else:
                messagebox.showerror("Invalid", "Invalid Username/Password")



# Class for the Home Page
class HomePage:
    def __init__(self, mainFrame, username, setting1, setting2, setting3):
        self.main = mainFrame
        self.user = username
        self.setting1 = setting1
        self.setting2 = setting2
        self.setting3 = setting3

        # Creating a new Tkinter Window
        self.home=Toplevel(self.main)
        self.home.title("Comprehensive Defence System")
        self.home.iconbitmap("img/shield.ico")
        self.home.geometry("1024x720")
        self.home.resizable(False, False)

        # Allocating space for the menu
        self.menu = Frame(self.home, bg="#232833")
        self.menu.pack(side=LEFT)
        self.menu.pack_propagate(False)
        self.menu.configure(width=300, height=720)

        # Allocating space for the screen
        self.screen = Frame(self.home, bg="#2F3644")
        self.screen.pack(side=LEFT)
        self.screen.pack_propagate(False)
        self.screen.configure(width=724, height=720)

        self.placeItems()

        Label(self.screen,text="Welcome to the Comprehensive Defence System", fg="#fff", bg="#2F3644", 
              font=('Helvetica, 14')).place(relx=0.25, rely=0.45)

        time.sleep(0.02) 

        self.main.withdraw()
        self.screen.mainloop()


    # -------------------------------------------------- SCREENS -------------------------------------------------
    # Anti Virus Screen
    def antivirusScreen(self):
        av_frame = Frame(self.screen, bg="#2F3644")
        av_frame.pack()
        av_frame.configure(width=724, height=720)

        self.scan = Button(av_frame, text="SCAN", bg="#45cd88", fg="#232833", padx=50, pady=10, border=0, 
                      font=('Helvetica, 12'), command=lambda: self.desktop_scan(av_frame))
        self.scan.place(relx=0.5, rely=0.5, anchor=CENTER)


    # Vulnerability Scanner Screen
    def vulnScanScreen(self):
        vulnerability_frame = Frame(self.screen, bg="#2F3644")
        vulnerability_frame.pack()
        vulnerability_frame.configure(width=724, height=720)

        self.vscan_button = Button(vulnerability_frame, text="SCAN", bg="#45cd88", fg="#232833", padx=50, pady=10, border=0, 
                      font=('Helvetica, 12'), command=lambda: self.vuln_scan(vulnerability_frame))
        self.vscan_button.place(relx=0.5, rely=0.5, anchor=CENTER)


    # Settings Screen
    def settingsScreen(self):
        settings_frame = Frame(self.screen, bg="#2F3644")
        settings_frame.pack()
        settings_frame.configure(width=724, height=720)

        decision = IntVar(value=self.setting1)
        decision2 = IntVar(value=self.setting2)
        decision3 = IntVar(value=self.setting3)
        setting1 = Checkbutton(settings_frame, text="\tTurn on automatic updates", bd=0, bg="#2F3644", fg="white", 
                            variable=decision, font=('Helvetica, 12'), selectcolor="#2F3644")
        setting2 = Checkbutton(settings_frame, text="\tOpen application when the computer starts up", bd=0, fg="white",
                            bg="#2F3644", variable=decision2, font=('Helvetica, 12'), selectcolor="#2F3644")
        setting3 = Checkbutton(settings_frame, text="\tTurn off notifications",bd=0, bg="#2F3644", fg="white",
                            variable=decision3, font=('Helvetica, 12'), selectcolor="#2F3644")

        setting1.place(relx=0.2, rely=0.3, anchor='w')
        setting2.place(relx=0.2, rely=0.4, anchor='w')
        setting3.place(relx=0.2, rely=0.5, anchor='w')

        save = Button(settings_frame, text="SAVE", bg="#45cd88", fg="#232833", padx=50, pady=10, border=0, 
                      font=('Helvetica, 12'), command=lambda: self.save_settings(self.user, decision.get(), decision2.get(), decision3.get()))
        save.place(relx=0.5, rely=0.9, anchor=CENTER)


    #--------------------------------------------------- SCREEN-RELATED FUNCTIONS -----------------------------------------
    def factory_reset(self):
        self.main.withdraw()

    def delete(self):
        for frame in self.screen.winfo_children():
            frame.destroy()    
    
    def hide_indicator(self):
        self.av.config(fg="#84888f")
        self.vuln.config(fg="#84888f")
        self.set.config(fg="#84888f")
        self.av_indicator.config(bg="#232833")
        self.vuln_indicator.config(bg="#232833")
        self.set_indicator.config(bg="#232833")

    def indicator(self, item1, item2, page):
        self.hide_indicator()
        item1.config(fg="white")
        item2.config(bg="#45cd88")
        self.delete()
        page()

    def logout(self):
        self.main.deiconify()
        self.home.destroy()

    def placeItems(self):

        welcome = Label(self.menu, text="Welcome !!!", bg="#232833", fg="white", font=('Helvetica, 10'))
        welcome.place(relx=0.27, rely=0.04, anchor=CENTER)

        Label(self.menu, text=self.user, bg="#232833", fg="white", font=('Helvetica, 14')).place(relx=0.25, rely=0.09, anchor=CENTER)

        self.av = Button(self.menu, text="Anti-Virus Scanner", bg="#232833", fg="#84888f", padx=15, pady=15, border=0, font=('Helvetica, 12'), 
                    cursor="hand2", command=lambda: self.indicator(self.av, self.av_indicator, self.antivirusScreen))
        self.vuln = Button(self.menu, text="Vulnerability Scanner", bg="#232833", fg="#84888f", highlightbackground="#2F3644",padx=15, pady=15, 
                    cursor="hand2", border=0, font=('Helvetica, 12'), command=lambda: self.indicator(self.vuln, self.vuln_indicator, self.vulnScanScreen))
        self.set = Button(self.menu, text="Settings & Privacy", bg="#232833", fg="#84888f", highlightbackground="#2F3644",padx=15, pady=15, 
                    cursor="hand2", border=0, font=('Helvetica, 12'), command=lambda: self.indicator(self.set, self.set_indicator, self.settingsScreen))
        self.out = Button(self.menu, text="Log Out", bg="#2f3644", fg="red", padx=50, pady=10, border=0, 
                          activebackground="red", activeforeground="#2f3644",font=('Helvetica, 12'),cursor="hand2", 
                          command=self.logout)

        self.av_indicator = Label(self.menu, text='', bg="#232833")
        self.av_indicator.place(relx=0.15, rely=0.3, anchor='w')
        self.vuln_indicator = Label(self.menu, text='', bg="#232833")
        self.vuln_indicator.place(relx=0.15, rely=0.45, anchor='w')
        self.set_indicator = Label(self.menu, text='', bg="#232833")
        self.set_indicator.place(relx=0.15, rely=0.6, anchor='w')

        self.av.place(relx=0.2, rely=0.3, anchor='w')
        self.vuln.place(relx=0.2, rely=0.45, anchor='w')
        self.set.place(relx=0.2, rely=0.6, anchor='w')
        self.out.place(relx=0.5, rely=0.9, anchor=CENTER)


    # ----------------------------------------------- FEATURE SPECIFIC FUNCTIONS -------------------------------------------
    def desktop_scan(self, frame):
        scanner = MF.AV()

        scanLabel = Label(frame, text="Scanning the Desktop directory", bg="#2F3644", fg="#ffffff",
                      font=('Helvetica, 12'), pady=5)
        scanLabel.place(relx=0.35, rely=0.55)
        progressBar = ttk.Progressbar(frame, orient=HORIZONTAL, length=400, mode='determinate')
        progressBar.place(relx=0.5, rely=0.7, anchor=CENTER)

        for x in range(5):
            progressBar['value'] += 20
            self.home.update_idletasks()
            time.sleep(0.5)

        progressBar.destroy()
        scanLabel.destroy()
        self.scan.place(relx=0.5, rely=0.2, anchor=CENTER)

        results = scanner.scanning("C:\\Users\\"+os.environ.get('USERNAME')+"\\Desktop")
        count = 0.32
        if len(results) > 2:
            for result in results:
                Label(frame, text=result, bg="#2F3644", fg="#ffffff",
                      font=('Helvetica, 12'), pady=5).place(relx=0.1, rely=count)
                count += 0.05


    def vuln_scan(self, frame):
        vuln_scanner = MF.VScanner()

        scanLabel = Label(frame, text="Discovering info about the OS", bg="#2F3644", fg="#ffffff",
                      font=('Helvetica, 12'), pady=5)
        scanLabel.place(relx=0.35, rely=0.55)
        progressBar = ttk.Progressbar(frame, orient=HORIZONTAL, length=400, mode='determinate')
        progressBar.place(relx=0.5, rely=0.7, anchor=CENTER)

        for x in range(5):
            progressBar['value'] += 20
            self.home.update_idletasks()
            time.sleep(0.5)

        progressBar.destroy()
        scanLabel.destroy()

        osValues = vuln_scanner.osDetection()

        scanLabel = Label(frame, text="Finding Directories with Whitespace", bg="#2F3644", fg="#ffffff",
                      font=('Helvetica, 12'), pady=5)
        scanLabel.place(relx=0.35, rely=0.55)
        progressBar = ttk.Progressbar(frame, orient=HORIZONTAL, length=400, mode='determinate')
        progressBar.place(relx=0.5, rely=0.7, anchor=CENTER)

        for x in range(5):
            progressBar['value'] += 20
            self.home.update_idletasks()
            time.sleep(0.5)

        progressBar.destroy()
        scanLabel.destroy()

        dir_values = vuln_scanner.dir_spaces()

        scanLabel = Label(frame, text="Performing Port Scan", bg="#2F3644", fg="#ffffff",
                      font=('Helvetica, 12'), pady=5)
        scanLabel.place(relx=0.35, rely=0.55)
        progressBar = ttk.Progressbar(frame, orient=HORIZONTAL, length=400, mode='determinate')
        progressBar.place(relx=0.5, rely=0.7, anchor=CENTER)

        for x in range(5):
            progressBar['value'] += 20
            self.home.update_idletasks()
            time.sleep(0.5)

        progressBar.destroy()
        scanLabel.destroy()
        self.vscan_button.place(relx=0.5, rely=0.1, anchor=CENTER)

        ports_open = vuln_scanner.portScan()

        Label(frame, text="OS INFORMATION", bg="#2F3644", fg="#45cd88",
                font=('Helvetica, 14'), pady=5).place(relx=0.1, rely=0.15)
        
        Label(frame, text="Operating System: "+ osValues[0] + " " + osValues[1], bg="#2F3644", fg="#ffffff",
                font=('Helvetica, 10'), pady=5).place(relx=0.1, rely=0.2)

        Label(frame, text="System Version: "+ osValues[2], bg="#2F3644", fg="#ffffff",
                font=('Helvetica, 10'), pady=5).place(relx=0.1, rely=0.23)
        
        Label(frame, text="This version will no longer be supported after " + osValues[3], bg="#2F3644", fg="#ffffff",
                font=('Helvetica, 10'), pady=5).place(relx=0.1, rely=0.27)

        Label(frame, text="Today's date is "+ str(date.today()), bg="#2F3644", fg="#ffffff",
                font=('Helvetica, 10'), pady=5).place(relx=0.1, rely=0.3)


        Label(frame, text="DIRECTORY WHITESPACE", bg="#2F3644", fg="#45cd88",
                font=('Helvetica, 14'), pady=5).place(relx=0.1, rely=0.37)
        
        Label(frame, text="There are " + str(len(dir_values)) + " directories with spaces in them", bg="#2F3644", 
              fg="#ffffff", font=('Helvetica, 10'), pady=5).place(relx=0.1, rely=0.42)
        
        if len(dir_values) > 0:
            Label(frame, text="Example: " + dir_values[0], bg="#2F3644", fg="#ffffff", font=('Helvetica, 8'), 
                pady=5).place(relx=0.1, rely=0.45)

        Label(frame, text="PORT SCAN RESULTS", bg="#2F3644", fg="#45cd88",
                font=('Helvetica, 14'), pady=5).place(relx=0.1, rely=0.52)
        
        count = 0.57
        if ports_open[0] == 0:
            Label(frame, text="No ports open", bg="#2F3644", fg="#ffffff",
                    font=('Helvetica, 10'), pady=5).place(relx=0.1, rely=count)
        else:
            for val in ports_open:
                Label(frame, text="Port "+ str(val) + " open", bg="#2F3644", fg="#ffffff",
                        font=('Helvetica, 10'), pady=5).place(relx=0.1, rely=count)
                count += 0.05

    def save_settings(self, user, d1, d2, d3):
        print("User: " + user + " " + str(d1)+" " + str(d2) + " " + str(d3))
        sql = MF.mySQL('192.168.56.101')
        print(sql.settingsUpdate(user, d1, d2, d3))