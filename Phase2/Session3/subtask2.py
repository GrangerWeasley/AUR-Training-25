import numpy as np
import matplotlib.pyplot as plt
import cv2

img = cv2.imread('C:\\Users\\youss\\OneDrive\\Desktop\\shapes.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
out = img.copy()

red_lower = np.array([100,0,0])
red_upper = np.array([255,80,80])

blue_lower = np.array([0,0,150])
blue_upper = np.array([100,100,255])

black_lower = np.array([0,0,0])
black_upper = np.array([50,50,50])

red_mask = cv2.inRange(img, red_lower, red_upper)
blue_mask = cv2.inRange(img, blue_lower, blue_upper)
black_mask = cv2.inRange(img, black_lower, black_upper)

out[blue_mask > 0] = [0,0,0]     #blue to black
out[red_mask > 0] = [0,0,255]    #red to blue
out[black_mask > 0] = [255,0,0]  #black to red

fig, axes = plt.subplots(1, 2)
axes[0].imshow(img)
axes[0].set_title('Original Image')
axes[0].axis('off')
axes[1].imshow(out)
axes[1].set_title('Processed Image')
axes[1].axis('off')
plt.show()