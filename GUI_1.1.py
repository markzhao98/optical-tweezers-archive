

import Tkinter as tk
import tkFileDialog as tkfd
import numpy as np
import cv2
import MMCorePy
import PIL.Image, PIL.ImageTk

# Initializing the microscope. --------------------

DEVICE = ['Camera', 'DemoCamera', 'DCam']

mmc = MMCorePy.CMMCore()
mmc.enableStderrLog(False)
mmc.enableDebugLog(False)
mmc.loadDevice(*DEVICE)
mmc.initializeDevice(DEVICE[0])
mmc.setCameraDevice(DEVICE[0])
mmc.setProperty(DEVICE[0], 'PixelType', '32bitRGB')

mmc.startContinuousSequenceAcquisition(1)

# ----------------------------------------

class App:
    def __init__(self, root, title):
        
        self.root = root
        self.root.title(title)

        self.btn_snapshot = tk.Button(self.root, width = 24, height = 4, 
                                      text='Snapshot', font='12',
                                      foreground = 'darkgreen',
                                      command = self.snapshot)
        self.btn_snapshot.pack(side = tk.LEFT)
        
        self.canvas = tk.Canvas(self.root, width = 512, height = 512)
        self.canvas.pack(side = tk.RIGHT)
        
        self.update()
        
        self.root.wm_protocol("WM_DELETE_WINDOW", self.out)
        
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
        
    def out(self):
        
        mmc.stopSequenceAcquisition()
        self.root.destroy()
        
pba = App(tk.Tk(), "The Optical Tweezer Program")
pba.root.mainloop()
