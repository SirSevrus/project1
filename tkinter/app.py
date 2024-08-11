import customtkinter as ctk
import os

class app:
    def __init__(self, geometry="400x400"):
        self.app = ctk.CTk()
        self.app.geometry(geometry)
        self.showFiles()
        self.app.mainloop()

    def listFiles(self, dirpath=""):
        items = os.listdir(dirpath)
        for i in items:
            if os.path.isfile(os.path.join(dirpath, i)) == False:
                items.remove(i)
        return items
    
    def showFiles(self):
        for i in self.listFiles(dirpath=r"C:\Users\sahil\Workspace\project1\data"):
            fileLabel = ctk.CTkLabel(self.app, text=i)
            fileLabel.pack()

app()