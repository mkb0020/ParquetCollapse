import sys
import os
import subprocess
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog, Label, Entry, Button, Tk
from tkinter import *


class WebsiteSubmissions(tk.Tk): #TKINTER GUI
    def __init__(self):
        super().__init__()  #  INITIALIZE TK WINDOW
        self.BackgroundDrip = "#C2CAE8" # BG COLOR
        self.title("WOULD YA LOOK AT THAT") #WOULD YOU JUST LOOK AT IT?
        self.configure(bg=self.BackgroundDrip)
        self.LabelDrip = {"bg": "#C2CAE8", "fg": "#000000", "font": ("Arial", 12)} #LABEL STYLE
        self.ButtonDrip = {"bg": "#FFFFFF", "fg": "#000000", "font": ("Arial", 11)} #BUTTON STYLE

    def GetFormData(self): #INPUT FORM
        Input = {} # BLANK CONTAINER FOR INPUT / FILE THAT YOU WANT TO SEE
        def ClickSubmit(): #SUBMIT BUTTON
            Input["File"] = File.get() #SELECT WHICH FILE: CONTACT ME SUBMISSIONS, ORDERS SUBMISSIONS, SUGGESTIONS BOX, GUESTBOOK
            Input["DateToday"] = datetime.now().strftime("%m-%d-%Y") #TIME STAMP FOR OUTPUT FILE NAME
            root.quit()
            root.destroy()
        def ClickCancel(): #CANCEL BUTTON
            Input["cancelled"] = True
            root.quit()
            root.destroy()

        root = self
        root.geometry("295x150")

        Label(root, text="Select File:", **self.LabelDrip).grid(row=0, column=0, pady=(15, 5), sticky="n") # LABEL

        File = ttk.Combobox( #DROP DOWN
            root,
            values=["Contact Me", "Orders", "Suggestions", "Guestbook"],
            state="readonly",
            font=("Arial", 11),
            width=20
        )
        File.grid(row=1, column=0, pady=5)
        File.current(0)

        ButtonFrame = tk.Frame(root, bg=self.BackgroundDrip) #BUTTON FRAME SO BUTTONS STAY CENTERED
        ButtonFrame.grid(row=2, column=0, pady=(15, 10))

        CancelButton = Button(ButtonFrame, text="CANCEL", width=12, command=ClickCancel, relief="raised", padx=10, pady=5, **self.ButtonDrip)
        CancelButton.pack(side="left", padx=6)

        SubmitButton = Button(ButtonFrame, text="SUBMIT", width=12, command=ClickSubmit, relief="raised", padx=10, pady=5, **self.ButtonDrip)
        SubmitButton.pack(side="left", padx=6)

        root.eval('tk::PlaceWindow . center') #CENTER FORM
        root.mainloop()
        return Input

    def GetSavePath(self, Input): # CREATE SAVE PATH WITH TODAY'S DATE
        BaseName = f"{Input['File']}_{Input['DateToday']}.csv"
        Tk().withdraw()
        SavePath = filedialog.asksaveasfilename( # SELECT SAVE LOCATION
            defaultextension=".csv",
            initialfile=BaseName,
            filetypes=[("CSV Files", "*.csv")]
        )
        return SavePath

    def GetCSV(self, Input, SavePath):
        ViewFile = Input['File']

        if ViewFile == "Contact Me":
            ParquetFilePath = r"C:\Users\mkb00\PROJECTS\GitRepos\PortfolioSite\data\submissions.parquet"
        elif ViewFile == "Orders":
            ParquetFilePath = r"C:\Users\mkb00\PROJECTS\GitRepos\PortfolioSite\data\orders.parquet"
        elif ViewFile == "Suggestions":
            ParquetFilePath = r"C:\Users\mkb00\PROJECTS\GitRepos\PortfolioSite\data\suggestions.parquet"
        elif ViewFile == "Guestbook":
            ParquetFilePath = r"C:\Users\mkb00\PROJECTS\GitRepos\PortfolioSite\data\guestbook.parquet"
        else:
            messagebox.showerror("Error", "No valid file selected.")
            sys.exit(0)

        try:
            if not os.path.exists(ParquetFilePath): #IF FILE DOESN"T EXIST, ABORT MISSION
                messagebox.showinfo(
                    "No Data Found",
                    f"🫙 The {ViewFile} file doesn’t exist yet.\n\nNo submissions to view right now!"
                )
                sys.exit(0)
            SelectedFile = pd.read_parquet(ParquetFilePath)
            if SelectedFile.empty: #IF FILE EXISTS BUT IT"S EMPTY, ABORT MISSION
                messagebox.showinfo(
                    "No Data Found",
                    f"📭 The {ViewFile} file exists but has no data yet.\n\nNo submissions to display."
                )
                sys.exit(0)
            SelectedFile.to_csv(SavePath, index=False) #IF FILE EXSTS AND HAS DATA, PROCEED TO COPY INFO OVER TO CSV FILE
        except Exception as e:
            messagebox.showerror(
                "Error Reading File",
                f"⚠️ Something went wrong while reading {ViewFile}.\n\nDetails:\n{e}"
            )
            sys.exit(0)

    def ShowFinalPopup(self, Input, SavePath): # POPUP MESSAGE ONCE NEW CSV IS CREATED
        FinalPopup = tk.Tk()
        FinalPopup.title("FLAWLESS VICTORY!")
        FinalPopup.configure(bg=self.BackgroundDrip)
        FinalPopup.geometry("360x130")

        FinalFormFrame = tk.Frame(FinalPopup, bg=self.BackgroundDrip, padx=16, pady=12)
        FinalFormFrame.pack(fill="both", expand=True)

        ViewFile = Input['File'] # WHICHEVER FILE IS SELECTED FROM THE FIRST FORM

        if ViewFile == "Contact Me":
            ParquetFile = "Contact Submissions Parquet File"
        elif ViewFile == "Orders":
            ParquetFile = "Orders Submissions Parquet File"
        elif ViewFile == "Suggestions":
            ParquetFile = "Suggestions Submissions Parquet File"
        elif ViewFile == "Guestbook":
            ParquetFile = "Guestbook Submissions Parquet File"
        else:
            messagebox.showerror("Error", "No valid file selected.") #FALLBACK
            return

        tk.Label( # FINAL MESSAGE
            FinalFormFrame,
            text=f"{ParquetFile}\n is now viewable as a CSV file!",
            **self.LabelDrip
        ).pack(anchor="center", pady=(0, 6))

        FinalButtonFrame = tk.Frame(FinalFormFrame, bg=self.BackgroundDrip)
        FinalButtonFrame.pack(fill="x", pady=(6, 0))

        def ViewFile():
            try:
                os.startfile(SavePath)  # WINDOWS
            except AttributeError:
                subprocess.call(["open", SavePath])  # MAC FALLBACK
            FinalPopup.destroy()
            sys.exit(0)

        def Okaaaay(): # EXIT
            FinalPopup.destroy()
            sys.exit(0)


        OkaaaayButton = tk.Button(FinalButtonFrame, text="CLOSE", width=16, command=Okaaaay, **self.ButtonDrip)
        OkaaaayButton.pack(side="left", padx=6)

        PeepButton = tk.Button(FinalButtonFrame, text="CHECK IT OUT", width=16, command=ViewFile, **self.ButtonDrip)
        PeepButton.pack(side="left", padx=6)

        FinalPopup.eval('tk::PlaceWindow . center')
        FinalPopup.mainloop()

    
    def RunIt(self): # TIE EVERYTHING TOGETHER
        FormData = self.GetFormData()
        if "cancelled" in FormData:
            self.destroy()
            sys.exit(0)
        SavePath = self.GetSavePath(FormData)
        self.GetCSV(FormData, SavePath)
        self.ShowFinalPopup(FormData, SavePath)

def ViewSubmissions(): #FULL SEND
    CheckItOut = WebsiteSubmissions()
    CheckItOut.RunIt()
    sys.exit()

if __name__ == "__main__":
    ViewSubmissions()



