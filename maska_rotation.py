import cv2
import numpy as np
from PIL import Image, ImageDraw
import math

background = cv2.imread('map.jpg')
hsv = cv2.cvtColor(background, cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
lower = np.array([0,50,50])
upper = np.array([75,255,255])

# Create a mask. Threshold the HSV image to get only yellow colors
mask = cv2.inRange(hsv, lower, upper)

img_old = Image.fromarray(background)
pixels = img_old.load()
draw = ImageDraw.Draw(img_old)
counter=0
k=0
for alpha in range (0,90):
  for x in range(0,img_old.size[0],15):
    for y in range(0,img_old.size[1],15):
      new_x = round(x*math.cos(alpha*math.pi/180) -y *math.sin(alpha*math.pi/180))
      new_y = round(x*math.sin(alpha*math.pi/180) +y *math.cos(alpha*math.pi/180))
      pi=0
      for q in range(3):
        color = (pixels[x, y][q]==0) 
        pi+=1
      if k%2 and pi==3:
        draw.rectangle([(new_x,new_y),(new_x+5,new_y+5)],fill=(255, 20, 147))
        counter+=1
      else:
        draw.ellipse([(new_x,new_y),(new_x+5,new_y+5)],fill=(210, 105, 30))
      k+=1
  img = np.asarray(img_old)
  result = cv2.bitwise_and(img,img, mask= mask)
  mask = result[..., 2] >0  # если считаем, что чем меньше - тем прозрачнее
  background[:,:][mask] = result[mask]  # не забываем про равенство размера!
  # answer = cv2.bitwise_or(cv2.imread('answer.jpg'),cv2.imread('test_photo.jpg'))
  cv2.imwrite('r'+str(alpha)+'.png',result)
  #im=Image.open('r1.png')
