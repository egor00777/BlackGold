import cv2
import numpy as np
from PIL import Image, ImageDraw

background = cv2.imread('test_photo.jpg')
hsv = cv2.cvtColor(background, cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
lower = np.array([0,50,50])
upper = np.array([75,255,255])

# Create a mask. Threshold the HSV image to get only yellow colors
mask = cv2.inRange(hsv, lower, upper)

img = Image.fromarray(background)

draw = ImageDraw.Draw(img)
k=0
for x in range(0,img.size[0],45):
  for y in range(0,img.size[1],45):
    if k%2:
      draw.rectangle([(x,y),(x+15,y+15)],fill=(255, 20, 147))
    else:
      draw.ellipse([(x,y),(x+15,y+15)],fill=(210, 105, 30))
    k+=1
img = np.asarray(img)

result = cv2.bitwise_and(img,img, mask= mask)

mask = result[..., 2] >0  # если считаем, что чем меньше - тем прозрачнее
background[:,:][mask] = result[mask]  # не забываем про равенство размера!
# answer = cv2.bitwise_or(cv2.imread('answer.jpg'),cv2.imread('test_photo.jpg'))

cv2.imwrite('r1.jpg',background)
im=Image.open('r1.jpg')