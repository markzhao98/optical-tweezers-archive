import Tkinter as tk
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
        
        self.canvas = tk.Canvas(self.root, width = 512, height = 512)
        self.canvas.pack()
        
        self.update()
        
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
        
        
pba = App(tk.Tk(), "The Optical Tweezer Program")
pba.root.mainloop()
