# Run Micro-Manager ------------------------------------------------------------

#import os
#os.startfile("C:\Program Files\Micro-Manager-1.4\ImageJ.exe")

import Tkinter as tk
import PyDAQmx
import numpy as np
import time
import csv

# The GUI ------------------------------------------------------------

class GUI:
    
    def __init__(self, root, title):
        
#        self.task_x = PyDAQmx.Task()
#        self.task_y = PyDAQmx.Task()
#        
#        self.task_x.CreateAOVoltageChan("/Dev1/ao1","",
#                           -10.0,10.0,PyDAQmx.DAQmx_Val_Volts,None)
#
#        self.task_y.CreateAOVoltageChan("/Dev1/ao0","",
#                           -10.0,10.0,PyDAQmx.DAQmx_Val_Volts,None)
#        
#        self.task_x.StartTask()
#        self.task_y.StartTask()
#        
#        self.value_x = -0.65  # Equilibrium x mirror voltage value
#        self.value_y = -0.05  # Equilibrium y mirror voltage value
#        
#        self.task_x.WriteAnalogScalarF64(1,10.0,self.value_x,None)
#        self.task_y.WriteAnalogScalarF64(0,10.0,self.value_y,None)
        
        self.root = root
        self.root.title(title)
        
        # A ----------------------------------------
        
        self.varA = tk.BooleanVar()
        self.varA.set(True)
        
        self.label_A = tk.Label(self.root, text = str((696,520)), font='12', 
                                height = 2, width = 16, 
                                relief = tk.FLAT)
        self.label_A.grid(row = 0, column=1)
        
        self.cbtn_A = tk.Checkbutton(self.root, relief = tk.GROOVE, 
                                     height = 2, width = 8, 
                                     text='Trap A', font='12', 
                                     variable = self.varA, 
                                     disabledforeground = 'black',
                                     state = tk.DISABLED)
        self.cbtn_A.grid(row = 0, column = 0, padx = 5, sticky = tk.W)
        
        # B ----------------------------------------
        
        self.varB = tk.BooleanVar()
        self.varB.set(True)
        
        self.X = 696
        self.Y = 520
        
        self.label_B = tk.Label(self.root, text = str((self.X, self.Y)), font='12', 
                                height = 2, width = 16, 
                                relief = tk.FLAT)
        self.label_B.grid(row = 1, column=1)
 
        self.btn_B = tk.Button(self.root, text = 'Set', font = '12', fg = 'orange', 
                               height = 1, width = 6, 
                               disabledforeground = 'slate grey',
                               state = tk.NORMAL, command = self.setbutton)
        self.btn_B.grid(row = 1, column=2, padx = 5)
        
        self.cbtn_B = tk.Checkbutton(self.root, relief = tk.GROOVE,
                                     height = 2, width = 8,
                                     text='Trap B', font='12', 
                                     variable = self.varB, 
                                     disabledforeground = 'black',
                                     state = tk.DISABLED)
        self.cbtn_B.grid(row = 1, column = 0, padx = 5, sticky = tk.W)
        
        # Done --------------------------------------------------
        
        self.btn_unset = tk.Button(self.root, text='Done setting', 
                                   font = '12', fg = 'salmon',
                                   disabledforeground = 'slate grey',
                                   height = 1, width = 12,
                                   command = self.done, state = tk.DISABLED)
        self.btn_unset.grid(row = 1, column = 3, padx = 20)
        
        # Oscillation config --------------------------------------------------
        
        self.label_osci = tk.Label(self.root, 
                                   text = "Oscillation Configuration - Trap B",
                                   font = '12', height = 2, width = 38, 
                                   relief = tk.RIDGE)
        self.label_osci.grid(row = 2, column = 0, columnspan = 3, 
                             padx = 5, pady = 10, sticky = tk.W)

        self.label_whichdir = tk.Label(self.root, text = "Direction", font = '12',
                                       height = 2, width = 14, relief = tk.FLAT)
        self.label_whichdir.grid(row = 3, column = 1)

        self.listbox_whichdir = tk.Listbox(self.root, selectmode=tk.BROWSE,
                                           height = 2, width = 14,
                                           exportselection=0)
        self.listbox_whichdir.insert(1, "Horizontal")
        self.listbox_whichdir.insert(2, "Vertical")
        self.listbox_whichdir.grid(row = 3, column = 2)
        
        self.label_freq = tk.Label(self.root, text = "Frequency [Hz]", font = '12',
                                   height = 2, width = 14, relief = tk.FLAT)
        self.label_freq.grid(row = 4, column = 1)
        
        self.label_freqrange = tk.Label(self.root, text = 'int (0,1000) >>',
                                        height = 2, width = 12, relief = tk.FLAT)
        self.label_freqrange.grid(row = 4, column = 0)
        
        self.entry_freq = tk.Entry(self.root, width = 14)
        self.entry_freq.grid(row = 4, column = 2)
        
        self.label_amp = tk.Label(self.root, text = "Amplitude [Pixel]", font = '12',
                                  height = 2, width = 14, relief = tk.FLAT)
        self.label_amp.grid(row = 5, column = 1)
        
        self.label_amprange = tk.Label(self.root, text = 'int (0,1000) >>', 
                                        height = 2, width = 12, relief = tk.FLAT)
        self.label_amprange.grid(row = 5, column = 0)

        self.entry_amp = tk.Entry(self.root, width = 14)
        self.entry_amp.grid(row = 5, column = 2)
        
        # Begin oscillation --------------------------------------------------
        
        self.btn_osci_begin = tk.Button(self.root, text = 'Begin', font = '12',
                                        fg = 'forest green', height = 4 , width = 10,
                                        disabledforeground = 'slate grey', 
                                        state = tk.NORMAL, command = self.oscibegin)
        self.btn_osci_begin.grid(row =2, rowspan = 2, column = 3, sticky = tk.S)
        
        # End oscillation --------------------------------------------------
        
        self.btn_osci_end = tk.Button(self.root, text = 'End', font = '12',
                                      fg = 'lime green', height = 2, width = 10,
                                      disabledforeground = 'slate grey', 
                                      state = tk.DISABLED, command = self.osciend)
        self.btn_osci_end.grid(row = 4, rowspan = 2, column = 3)
        
        # update --------------------------------------------------
        
        self.update()
        
        # shutdown --------------------------------------------------
         
        self.root.wm_protocol("WM_DELETE_WINDOW", self.out)
        
    # -------------------------------------------------------
        
    def update(self): 
        with open("coords.csv") as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                self.X_temp = row[1]
                self.Y_temp = row[2]
        
        if self.X != int(self.X_temp) or self.Y != int(self.Y_temp):
            self.ifclick = True
            self.X = int(self.X_temp)
            self.Y = int(self.Y_temp)
        else:
            self.ifclick = False

        self.root.after(5, self.update)
        
    # -------------------------------------------------------

    def setbutton(self):
        self.btn_B.config(relief = tk.SUNKEN, state = tk.DISABLED)
        self.btn_unset.config(state = tk.NORMAL)
        self.btn_osci_begin.config(state = tk.DISABLED)
        if self.ifclick == True:
            self.label_B.config(text = str((self.X, self.Y)))
        self.solve = self.root.after(2, self.setbutton)
        
    # -------------------------------------------------------
        
    def done(self):
        self.btn_B.config(relief = tk.RAISED, state = tk.NORMAL)
        self.btn_unset.config(state = tk.DISABLED)
        self.btn_osci_begin.config(state = tk.NORMAL)
        self.root.after_cancel(self.solve)

    # -------------------------------------------------------

    def oscibegin(self):
        if (len(self.listbox_whichdir.curselection()) == 1 and 
            self.isint(self.entry_freq.get()) == True and 
            self.isint(self.entry_amp.get()) == True):
            if (int(self.entry_freq.get()) > 0 and 
                int(self.entry_freq.get()) <= 999 and 
                int(self.entry_amp.get()) > 0 and 
                int(self.entry_amp.get()) <= 999):
                
                self.btn_B.config(state = tk.DISABLED)
                self.listbox_whichdir.config(state = tk.DISABLED)
                self.entry_freq.config(state = tk.DISABLED)
                self.entry_amp.config(state = tk.DISABLED)
                self.btn_osci_begin.config(relief = tk.SUNKEN, state = tk.DISABLED)
                self.btn_osci_end.config(state = tk.NORMAL)
                
                self.freq = int(self.entry_freq.get())
                self.amp = int(self.entry_amp.get())
                
    # -------------------------------------------------------
    
    def osciend(self):
        self.btn_osci_begin.config(relief = tk.RAISED, state = tk.NORMAL)
        self.btn_osci_end.config(state = tk.DISABLED)
        self.btn_B.config(state = tk.NORMAL)
        self.listbox_whichdir.config(state = tk.NORMAL)
        self.entry_freq.config(state = tk.NORMAL)
        self.entry_amp.config(state = tk.NORMAL)

    # -------------------------------------------------------
    
    def isint(self, stuff):
      try:
        float(stuff)
        return True
      except ValueError:
        return False
        
    # -------------------------------------------------------
    
    def out(self):
#        self.task_x.StopTask()
#        self.task_y.StopTask()
        self.root.destroy()
        
# ------------------------------------------------------------
        
gui = GUI(tk.Tk(), "The Optical Tweezer Program - Galvo Version")
gui.root.mainloop()
