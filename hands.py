import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

xsize = 1920
ysize = 1080

fig, cave = plt.subplots()
fig.set_size_inches(xsize/100, ysize/100)
cave.set_xlim(0, xsize)
cave.set_ylim(0, ysize)
cave.set_axis_off()

hand_width = int(640/5)
hand_height = int(480/5)

tx = np.random.randint(xsize-hand_width)
ty = np.random.randint(ysize-hand_height)
rect = cave.add_patch(Rectangle((tx, ty),
                                hand_width, hand_height,
                                edgecolor='red', facecolor='none', lw=2))
plt.savefig('cave.png', facecolor='k')
cave_img = cv2.imread('cave.png')

#cv2.rectangle(wall_img, pt1=(tx,ty), pt2=(tx+100,ty+100), color=(0,0,255), thickness=5)
cv2.imshow("Digital Cave of Hands", cave_img)

color = [np.random.randint(255), np.random.randint(255), np.random.randint(255)]

while True:
    ret, img = cam.read()

    hsvim = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    skinRegionHSV = cv2.inRange(hsvim, lower, upper)
    blurred = cv2.blur(skinRegionHSV, (2,2))
    ret, thresh = cv2.threshold(blurred,0,1,cv2.THRESH_BINARY)

    #color_thresh = np.zeros(img.shape)
    color_thresh = img
    color_thresh[:, :, 0] = thresh*color[0]
    color_thresh[:, :, 1] = thresh*color[1]
    color_thresh[:, :, 2] = thresh*color[2]

    #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #contours = max(contours, key=lambda x: cv2.contourArea(x))
    #contour_only = np.zeros((480, 640, 3))
    #cv2.drawContours(contour_only, [contours], -1, (255, 255, 0), 2)

    #wall.imshow(thresh, extent=(tx, tx + hand_width, ty, ty + hand_height), cmap='gray')
    #plt.savefig('wall.png', facecolor='k')
    #wall_img = cv2.imread('wall.png')
    #cv2.imshow("wall", wall_img)

    show = cv2.cvtColor(color_thresh, cv2.COLOR_BGR2RGB)
    cv2.imshow("Hand", show)
    k = cv2.waitKey(1)
    # enter key
    if k == 13:
        #print(thresh.shape)
        #hand = cv2.resize(thresh, dsize=(160, 120))
        #cv2.imshow('CaveWall', hand)
        cave.imshow(color_thresh, extent=(tx, tx + hand_width, ty, ty + hand_height))
        rect.remove()
        tx = np.random.randint(xsize-hand_width)
        ty = np.random.randint(ysize-hand_height)
        rect = cave.add_patch(Rectangle((tx, ty), hand_width, hand_height, edgecolor='red', facecolor='none', lw=2))
        plt.savefig('cave.png', facecolor='k')
        cave_img = cv2.imread('cave.png')
        cv2.imshow("Digital Cave of Hands", cave_img)
        color = [np.random.randint(255), np.random.randint(255), np.random.randint(255)]
    # space bar
    if k == 32:
        cam.release()
        cv2.destroyAllWindows()
        date = str(datetime.now())
        datename = ''
        for char in date:
            if char != '-' and char != ':' and char != '.' and char != ' ':
                datename += char
        plt.savefig(f'cave{datename}.png', facecolor='k')
        #plt.show()
        break
