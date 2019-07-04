import cv2
import numpy as np
import MMCorePy

posList = []
def onMouse(event, x, y, flags, param):
   global posList
   if event == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        print((x,y))

DEVICE = ['Camera', 'DemoCamera', 'DCam']

if __name__ == '__main__':
    mmc = MMCorePy.CMMCore()
    mmc.enableStderrLog(False)
    mmc.enableDebugLog(False)
    mmc.loadDevice(*DEVICE)
    mmc.initializeDevice(DEVICE[0])
    mmc.setCameraDevice(DEVICE[0])
    mmc.setProperty(DEVICE[0], 'PixelType', '32bitRGB')

    cv2.namedWindow('Video')
    mmc.startContinuousSequenceAcquisition(1)
    while True:
        if mmc.getRemainingImageCount() > 0:
            rgb32 = mmc.getLastImage()
            bgr = rgb32.view(dtype=np.uint8).reshape(
                rgb32.shape[0], rgb32.shape[1], 4)[..., :3]
            cv2.imshow('Video', bgr)
            cv2.setMouseCallback('Video', onMouse)
            
        # Press <ESC> to end the program
        if cv2.waitKey(20) == 27:
            break
        
    cv2.destroyAllWindows()
    mmc.stopSequenceAcquisition()
    mmc.reset()
