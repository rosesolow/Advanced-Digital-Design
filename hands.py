import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

fig, wall = plt.subplots()
fig.set_size_inches(18, 10)
wall.set_xlim(0, 1800)
wall.set_ylim(0, 1000)
wall.set_axis_off()

tx = np.random.randint(1700)
ty = np.random.randint(900)
rect = wall.add_patch(Rectangle((tx,ty),100,100,edgecolor='red',facecolor='none',lw=4))
plt.savefig('wall.png',facecolor='k')
wall_img = cv2.imread('wall.png')

#cv2.rectangle(wall_img, pt1=(tx,ty), pt2=(tx+100,ty+100), color=(0,0,255), thickness=5)
cv2.imshow("wall", wall_img)

while True:
    ret, img = cam.read()
    hsvim = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    skinRegionHSV = cv2.inRange(hsvim, lower, upper)
    blurred = cv2.blur(skinRegionHSV, (2,2))
    ret, thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY)
    #cv2.imshow("thresh", thresh)
    k = cv2.waitKey(20)
    # enter key
    if k == 13:
        #print(thresh.shape)
        #hand = cv2.resize(thresh, dsize=(160, 120))
        #cv2.imshow('CaveWall', hand)
        wall.imshow(thresh, extent=(tx, tx + 100, ty, ty + 100), cmap='gray')
        rect.remove()
        tx = np.random.randint(1700)
        ty = np.random.randint(900)
        rect = wall.add_patch(Rectangle((tx, ty), 100, 100, edgecolor='red', facecolor='none', lw=4))
        plt.savefig('wall.png',facecolor='k')
        wall_img = cv2.imread('wall.png')
        cv2.imshow("wall", wall_img)
    # space bar
    if k == 32:
        cam.release()
        cv2.destroyAllWindows()
        #plt.show()
        break
