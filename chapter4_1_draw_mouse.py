import cv2
import numpy as np


def mouse_event(event, x, y, flags, src):
    global radius, center_pos, draw_flag

    new_img = src.copy()
    if event == cv2.EVENT_FLAG_LBUTTON:
        draw_flag = True
        center_pos = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE:
        if draw_flag:
            cv2.circle(new_img, center_pos,
                       max(abs(center_pos[0]-x), abs(center_pos[1]-y)),
                       (255, 0, 0), 2)
            cv2.imshow("draw", new_img)
    elif event == cv2.EVENT_LBUTTONUP:
        draw_flag = False
        cv2.circle(src, center_pos,
                   max(abs(center_pos[0] - x), abs(center_pos[1] - y)),
                   (255, 0, 0), 2)
        cv2.imshow("draw", src)

    elif event == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            radius += 1
        elif radius > 1:
            radius -= 1

draw_flag = False
center_pos = (0, 0)
radius = 3
src = np.full((500, 500, 3), 255, dtype=np.uint8)

cv2.imshow("draw", src)
cv2.setMouseCallback("draw", mouse_event, src)
cv2.waitKey(0)