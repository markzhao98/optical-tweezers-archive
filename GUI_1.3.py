import Tkinter as tk
import tkFileDialog as tkfd
import numpy as np
import cv2
import MMCorePy
import PIL.Image, PIL.ImageTk

# Initializing the microscope. ------------------------------

DEVICE = ['Camera', 'DemoCamera', 'DCam']

mmc = MMCorePy.CMMCore()
mmc.enableStderrLog(False)
mmc.enableDebugLog(False)
mmc.loadDevice(*DEVICE)
mmc.initializeDevice(DEVICE[0])
mmc.setCameraDevice(DEVICE[0])
mmc.setProperty(DEVICE[0], 'PixelType', '32bitRGB')

mmc.startContinuousSequenceAcquisition(1)

# ------------------------------------------------------------

class App:
    
    def __init__(self, root, title):
        
        self.root = root
        self.root.title(title)
        
        # checkbutton 1 & label 1 & button 1 --------------------
        
        self.var1 = tk.BooleanVar()
        self.var1.set(True)
        
        self.label_1 = tk.Label(self.root, text = str((256,256)), font='12', 
                                 height = 2, width = 16, 
                                 relief = tk.FLAT)
        self.label_1.grid(row = 0, column=1)
        
        self.btn_1 = tk.Button(self.root, text = 'Set', font = '12', fg = 'orange', 
                               height = 1, width = 6, 
                               disabledforeground = 'grey', 
                               state = tk.NORMAL, command = self.setbutton_1)
        self.btn_1.grid(row = 0, column=2)
        
        self.cbtn_1 = tk.Checkbutton(self.root, relief = tk.GROOVE, 
                                     height = 2, width = 8, 
                                     text='Trap 1', font='12', 
                                     variable = self.var1, 
                                     disabledforeground = 'black',
                                     state = tk.DISABLED)
        self.cbtn_1.grid(row = 0, column = 0, padx = 5)
        
        # checkbutton 2 & label 2 & button 2 --------------------
        
        self.var2 = tk.BooleanVar()
        
        self.label_2 = tk.Label(self.root, text = 'None', font='12', 
                         height = 2, width = 16, 
                         relief = tk.FLAT)
        self.label_2.grid(row = 1, column=1)
 
        self.btn_2 = tk.Button(self.root, text = 'Set', font = '12', fg = 'orange', 
                               height = 1, width = 6, 
                               disabledforeground = 'grey',
                               state = tk.DISABLED, command = self.setbutton_2)
        self.btn_2.grid(row = 1, column=2)
        
        self.cbtn_2 = tk.Checkbutton(self.root, relief = tk.GROOVE,
                             height = 2, width = 8,
                             text='Trap 2', font='12', 
                             variable = self.var2,  
                             command = self.enable_2)
        self.cbtn_2.grid(row = 1, column = 0, padx = 5)
        
        # checkbutton 3 & label 3 & button 3 --------------------
        
        self.var3 = tk.BooleanVar()
        
        self.label_3 = tk.Label(self.root, text = 'None', font='12', 
                         height = 2, width = 16, 
                         relief = tk.FLAT)
        self.label_3.grid(row = 2, column=1)
 
        self.btn_3 = tk.Button(self.root, text = 'Set', font = '12', fg = 'orange', 
                               height = 1, width = 6, 
                               disabledforeground = 'grey',
                               state = tk.DISABLED, command = self.setbutton_3)
        self.btn_3.grid(row = 2, column=2)
        
        self.cbtn_3 = tk.Checkbutton(self.root, relief = tk.GROOVE,
                             height = 2, width = 8,
                             text='Trap 3', font='12', 
                             variable = self.var3, 
                             command = self.enable_3)
        self.cbtn_3.grid(row = 2, column = 0, padx = 5)
        
        # checkbutton 2 & label 2 & button 2 --------------------
        
        self.var4 = tk.BooleanVar()
        
        self.label_4 = tk.Label(self.root, text = 'None', font='12', 
                         height = 2, width = 16, 
                         relief = tk.FLAT)
        self.label_4.grid(row = 3, column=1)
 
        self.btn_4 = tk.Button(self.root, text = 'Set', font = '12', fg = 'orange', 
                               height = 1, width = 6, 
                               disabledforeground = 'grey',
                               state = tk.DISABLED, command = self.setbutton_4)
        self.btn_4.grid(row = 3, column=2)
        
        self.cbtn_4 = tk.Checkbutton(self.root, relief = tk.GROOVE,
                             height = 2, width = 8,
                             text='Trap 4', font='12', 
                             variable = self.var4, 
                             command = self.enable_4)
        self.cbtn_4.grid(row = 3, column = 0, padx = 5)
        
        # real-time coords labels ----------------------------------------
        
        self.word_label = tk.Label(self.root, text = "Real-time cursor location: ",
                                  font = '12', relief = tk.FLAT)
        self.word_label.grid(row = 4, column = 0, columnspan = 2, 
                             sticky=tk.W+tk.E)
        
        self.cur_label = tk.Label(self.root, font = '12', text = '--', 
                                  height = 2, width = 10, 
                                  relief = tk.FLAT)
        self.cur_label.grid(row = 4, column =2, sticky=tk.W)
        
        # snapshot button ----------------------------------------
        
        self.btn_snapshot = tk.Button(self.root,
                                      text='Snapshot', font='12',
                                      foreground = 'darkgreen', 
                                      height = 2,
                                      command = self.snapshot)
        
        self.btn_snapshot.grid(row = 5, column = 0, columnspan = 3, 
                               sticky=tk.W+tk.E+tk.N+tk.S, pady=20, padx = 5)
        
        # canvas --------------------------------------------------
        
        self.canvas = tk.Canvas(self.root, width = 509, height = 509)
        
        self.canvas.grid(column = 4, row = 0, rowspan = 6,
                         sticky=tk.W+tk.E+tk.N+tk.S, 
                         padx = 5, pady = 10)
        
        self.update()
        
        # mouse stuff --------------------------------------------------
        
        self.in_var = False
        
        self.canvas.bind('<Enter>', self.enter)
        self.canvas.bind('<Leave>', self.leave)
        self.root.bind('<Motion>', self.motion)
        
        # shutdown --------------------------------------------------
        
        self.root.wm_protocol("WM_DELETE_WINDOW", self.out)
        
    # -------------------------------------------------------
        
    def update(self):
        
        if mmc.getRemainingImageCount() > 0:
            rgb32 = mmc.getLastImage()
            bgr = rgb32.view(dtype=np.uint8).reshape(
                    rgb32.shape[0], rgb32.shape[1], 4)[..., :3]
            prephoto = bgr
        else:
            prephoto = cv2.imread('blank.png')
        
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(prephoto))
        
        self.canvas.photo = photo
        
        self.canvas.create_image(0, 0, image = photo, anchor = tk.NW)
        
        self.root.after(1, self.update)
        
    # -------------------------------------------------------
        
    def snapshot(self):
        
        if mmc.getRemainingImageCount() > 0:
            rgb32 = mmc.getLastImage()
            bgr = rgb32.view(dtype=np.uint8).reshape(
                    rgb32.shape[0], rgb32.shape[1], 4)[..., :3]
            snap = bgr
        else:
            snap = cv2.imread('blank.png')
        
        output = tkfd.asksaveasfilename(initialdir = "/", 
                                        title = "Save JPEG file only", 
                                        defaultextension='.jpg', 
                                        filetypes = (("JPEG","*.jpg"),
                                                     ("","*.??")))
        
        cv2.imwrite(output, snap)

    # -------------------------------------------------------

    def enable(self, whichvar, whichlabel, whichbutton):
        if whichvar.get() == True:
            whichbutton.config(state=tk.NORMAL)
            whichlabel.config(text = str((256,256)))
        elif whichvar.get() == False:
            whichbutton.config(state=tk.DISABLED)
            whichlabel.config(text = 'None')
        
    def enable_2(self):
        self.enable(self.var2, self.label_2, self.btn_2)
        
    def enable_3(self):
        self.enable(self.var3, self.label_3, self.btn_3)
    
    def enable_4(self):
        self.enable(self.var4, self.label_4, self.btn_4)    

    # -------------------------------------------------------

    def setbutton(self, whichlabel, whichbutton):
        self.root.config(cursor = 'plus')
        self.root.config(cursor = 'arrow')
        
    def setbutton_1(self):
        self.setbutton(self.label_1, self.btn_1)
    
    def setbutton_2(self):
        self.setbutton(self.label_2, self.btn_2)
    
    def setbutton_3(self):
        self.setbutton(self.label_3, self.btn_3)
    
    def setbutton_4(self):
        self.setbutton(self.label_4, self.btn_4)

    # -------------------------------------------------------

    def enter(self, event):
        self.in_var = True
        
    def leave(self, event):
        self.in_var = False

    def motion(self, event):
        if self.in_var == True:
            self.x, self.y = event.x, event.y
            self.cur_label.config(text = '({}, {})'.format(self.x, self.y))
        if self.in_var == False:
            self.cur_label.config(text = '--')

    # -------------------------------------------------------
        
    def out(self):
        mmc.stopSequenceAcquisition()
        self.root.destroy()
        
# ------------------------------------------------------------
        
pba = App(tk.Tk(), "The Optical Tweezer Program")
pba.root.mainloop()
