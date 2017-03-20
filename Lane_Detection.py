
"""
	Title:	Lane detection algorithm
	Author:	Martin Lippl
"""



import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

from moviepy.editor import VideoFileClip




"""
	Helper Functions
"""

def grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, [vertices], ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=8):

	left_lines = []
	right_lines = []

	for line in lines:
		for x1,y1,x2,y2 in line:
			slope = (y2-y1)/(x2-x1)
			if (slope < -0.1):
				left_lines.append(line)
			elif (slope > 0.1):
				right_lines.append(line)

	#Conversion into numpy-arrays
	left_lines = np.array(left_lines)
	right_lines = np.array(right_lines)

	# Left lane:
	m_left = 0
	b_left = 0
	acc_m_left = 0
	acc_b_left = 0

	# y = m*x + b 
	# b = y - m*x

	for line in left_lines:
		for x1,y1,x2,y2 in line:
			m_left = (y2-y1)/(x2-x1)
			b_left = y2-m_left*x2 
			acc_m_left += m_left
			acc_b_left += b_left
	
	avg_m_left = acc_m_left/left_lines.shape[0]
	avg_b_left = acc_b_left/left_lines.shape[0]

	# x = 1/m*y-b/m
	# Evaluate this equation for y=325 and y=540

	left_x1 = int( 325. / avg_m_left - avg_b_left / avg_m_left )
	left_x2 = int( 540. / avg_m_left - avg_b_left / avg_m_left )

	cv2.line(img, (left_x1, 325), (left_x2, 540), color, thickness)

	# Right lane:
	m_right = 0
	b_right = 0
	acc_m_right = 0
	acc_b_right = 0

	for line in right_lines:
		for x1,y1,x2,y2 in line:
			m_right = (y2-y1)/(x2-x1)
			b_right = y2-m_right*x2 
			acc_m_right += m_right
			acc_b_right += b_right
	
	avg_m_right = acc_m_right/right_lines.shape[0]
	avg_b_right = acc_b_right/right_lines.shape[0]

	right_x1 = int( 325. / avg_m_right - avg_b_right / avg_m_right )
	right_x2 = int( 540. / avg_m_right - avg_b_right / avg_m_right )

	cv2.line(img, (right_x1, 325), (right_x2, 540), color, thickness)


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img


def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    return cv2.addWeighted(initial_img, α, img, β, λ)






# Image Processing Pipeline
def pipeline(original_img):

	low_threshold = 70
	high_threshold = 200
	kernel_size = 5

	#apex = [480, 300]
	left_top = [460, 325]
	right_top = [500, 325]
	left_bottom = [0, 540]
	right_bottom = [960, 540]

	tmp_img = original_img
	tmp_img = grayscale(original_img)
	tmp_img = gaussian_blur(tmp_img, kernel_size)
	tmp_img = canny(tmp_img, low_threshold, high_threshold)

	#vertices = np.append(right_bottom, [apex, left_bottom])
	#vertices = np.array([right_bottom, apex, left_bottom], np.int32)
	vertices = np.array([right_bottom, right_top, left_top, left_bottom], np.int32)
	tmp_img = region_of_interest(tmp_img, vertices)
	tmp_img = hough_lines(tmp_img, rho=1., theta=np.pi/90., threshold=10, min_line_len=10, max_line_gap=200)
	tmp_img = weighted_img(tmp_img, original_img)

	return tmp_img




# Video processing block

clip = VideoFileClip('./solidWhiteRight.mp4')
#clip = VideoFileClip('./solidYellowLeft.mp4')

output_handel = 'test_video.mp4'

output_stream = clip.fl_image(pipeline)
output_stream.write_videofile(output_handel, audio=False)
"""


# Image processing block

#original_image = mpimg.imread('test_images/solidWhiteRight.jpg')
original_image = mpimg.imread('test_images/solidWhiteRight.jpg')
	
#print('This image is:', type(masked_image), 'with dimesions:', masked_image.shape)
plt.imshow(pipeline(original_image))
plt.show()

"""









"""
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
    
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """