import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

from epmc.globalParams import g


class ResetSetupFrame(tk.Frame):
  def __init__(self, parentFrame):
    super().__init__(master=parentFrame)

    self.label = tb.Label(self, text="RESET ALL PARAMETERS", font=('Monospace',16, 'bold') ,bootstyle="dark")
    self.frame = tb.Frame(self)

    #create widgets to be added to frame1
    buttonStyle = tb.Style()
    buttonStyleName = 'primary.TButton'
    buttonStyle.configure(buttonStyleName, font=('Monospace',10,'bold'))
    self.resetButton = tb.Button(self.frame, text="RESET ALL PARAMETERS",
                               style=buttonStyleName, padding=20,
                               command=self.open_reset_dialog_event)

    #add framed widgets to frame
    self.resetButton.pack(side='top', expand=True, fill="both")

    #add frame1, frame2 and frame3 to MainFrame
    self.label.pack(side="top", fill="x", padx=(220,0), pady=(5,0))
    self.frame.place(relx=0.5, rely=0.5, anchor="center")


  def open_reset_dialog_event(self):
    # isSuccessful = self.resetAllParams()
    dialog = messagebox.askquestion("Form",
                          "This will reset all parameters on the controller's EEPROM to default.\nAre you sure you want to continue?", 
                          icon ='question')

    if dialog == "yes":
      isSuccessful = self.resetAllParams()
      if isSuccessful:
        messagebox.showinfo("Form",
                          "SUCCESS:\n\nParameters Reset was successful", 
                          icon ='info')
      else:
        messagebox.showinfo("Form",
                          "ERROR:\n\nSomething went wrong\nAttempt to reset was unsuccessful\nTry again", 
                          icon ='error')


  def resetAllParams(self):
    isSuccessful = g.serClient.send("/reset")
    return isSuccessful
