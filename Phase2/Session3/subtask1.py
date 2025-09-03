import cv2
import numpy as np
import matplotlib.pyplot as plt

def convolve(img,kernel):
    final = np.zeros_like(img)
    kernel=np.array(kernel)
    k_size=kernel.shape[0]
    if k_size%2==0:
        raise ValueError("kernel has to be odd ")
    
    image = np.pad(img, (( k_size//2 , k_size//2),(k_size//2,k_size//2)),mode='constant')

    sliced_image=np.zeros((k_size,k_size))
    rows=final.shape[0]
    col=final.shape[1]

    for i in range (0,rows):
        for j in range(0,col):
            #array[row_start:row_stop:row_step, col_start:col_stop:col_step]
            sliced_image = image[i:i+k_size:1 , j:j+k_size:1]
            final[i,j] = np.sum(sliced_image * kernel)
    return final

img=cv2.imread('C:\\Users\\youss\\OneDrive\\Desktop\\image.png',cv2.IMREAD_GRAYSCALE)
fig,axes=plt.subplots(2,2,figsize=(8,8))
axes[0,0].imshow(img,cmap='gray')
axes[0,0].set_title("Original Image")
axes[0,0].axis('off')
axes[0, 1].imshow(convolve(img, np.ones((5, 5)) / 25), cmap='gray')
axes[0, 1].set_title('Box Filter')
axes[0, 1].axis('off')
axes[1,0].imshow(convolve(img,[[-1,0,1],[-2,0,2],[-1,0,1]]),cmap='gray')
axes[1,0].set_title("Horizontal Sobel filter")
axes[1,0].axis('off')
axes[1,1].imshow(convolve(img,[[-1,-2,-1],[0,0,0],[1,2,1]]),cmap='gray')
axes[1,1].set_title("Vertical Sobel filter")
axes[1,1].axis('off')

plt.show()