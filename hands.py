import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from datetime import datetime

cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# size of projected screen
xsize = 1920*1.275
ysize = 1080*1.275

# set up figure for projected image
fig, cave = plt.subplots()
fig.set_size_inches(xsize/100, ysize/100)
cave.set_xlim(0, xsize)
cave.set_ylim(0, ysize)
cave.set_axis_off()

# scale down hand image
scale = 2.2
hand_width = int(640/scale)
hand_height = int(480/scale)

# random generate xy location for new hand image with red rectangle border
tx = np.random.randint(xsize-hand_width)
ty = np.random.randint(ysize-hand_height)
rect = cave.add_patch(Rectangle((tx, ty),
                                hand_width, hand_height,
                                edgecolor='red', facecolor='none', lw=2))

# save figure and display
plt.savefig('cave.png', facecolor='k', bbox_inches='tight')
cave_img = cv2.imread('cave.png')
#cv2.rectangle(wall_img, pt1=(tx,ty), pt2=(tx+100,ty+100), color=(0,0,255), thickness=5)
cv2.imshow("Digital Cave of Hands", cave_img)

# generate random color and randomly select style (0 or 1 for thresh or contour)
color = [np.random.randint(255), np.random.randint(255), np.random.randint(255)]
style = np.random.randint(2)

while True:
    ret, img = cam.read()
    img = cv2.flip(img,1)

    # threshold image to find hand
    hsvim = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    skinRegionHSV = cv2.inRange(hsvim, lower, upper)
    blurred = cv2.blur(skinRegionHSV, (2,2))
    ret, thresh = cv2.threshold(blurred,0,1,cv2.THRESH_BINARY)

    # colorize thresh or contour
    hand = img * 0
    if style:
        hand[:, :, 0] = thresh*color[0]
        hand[:, :, 1] = thresh*color[1]
        hand[:, :, 2] = thresh*color[2]
    else:
        # find contours and draw on black background
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contours = max(contours, key=lambda x: cv2.contourArea(x))
        cv2.drawContours(hand, contours, -1, color, 4)

    # shows hand in rectangle on figure, but laggy cuz of figure resaving
    #wall.imshow(thresh, extent=(tx, tx + hand_width, ty, ty + hand_height), cmap='gray')
    #plt.savefig('wall.png', facecolor='k')
    #wall_img = cv2.imread('wall.png')
    #cv2.imshow("wall", wall_img)

    # display hand image
    cv2.imshow("Hand", cv2.cvtColor(hand, cv2.COLOR_BGR2RGB))
    k = cv2.waitKey(1)
    # hit enter key to capture hand image and place on figure
    if k == 13:
        cave.imshow(hand, extent=(tx, tx + hand_width, ty, ty + hand_height))
        # remove previous rect and create new one at random loc
        rect.remove()
        tx = np.random.randint(xsize-hand_width)
        ty = np.random.randint(ysize-hand_height)
        print(tx)
        print(ty)
        print('')
        rect = cave.add_patch(Rectangle((tx, ty),
                                        hand_width, hand_height,
                                        edgecolor='red', facecolor='none', lw=2))

        # display figure
        plt.savefig('cave.png', facecolor='k',bbox_inches='tight')
        cave_img = cv2.imread('cave.png')
        cv2.imshow("Digital Cave of Hands", cave_img)

        # random generate color and style
        color = [np.random.randint(255), np.random.randint(255), np.random.randint(255)]
        style = np.random.randint(3)

    # hit space bar to exit program and save final figure under unique datetime filename
    if k == 32:
        cam.release()
        cv2.destroyAllWindows()
        date = str(datetime.now())
        datename = ''
        for char in date:
            if char != '-' and char != ':' and char != '.' and char != ' ':
                datename += char
        plt.savefig(f'cave{datename}.png', facecolor='k',bbox_inches='tight')
        break
