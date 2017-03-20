import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import cv2

image = mpimg.imread('exit-ramp.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

#plt.imshow(gray, cmap='gray')

low_threshold = 70
high_threshold = 200

kernel_size = 3

edges = cv2.Canny(gray, low_threshold, high_threshold)

#plt.imshow(edges)
plt.imshow(edges, cmap='gray')

plt.show()


