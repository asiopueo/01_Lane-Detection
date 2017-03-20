#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
#matplotlib inline


from moviepy.editor import VideoFileClip
#from IPython.core.display import HTML, display



def process_image(img):
	mask = np.zeros_like(img)

	if len(img.shape) > 2:
		channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
		ignore_mask_color = (255,) * channel_count
	else:
		ignore_mask_color = 255
 
	apex = [480, 300]
	left_bottom = [0, 540]
	right_bottom = [960, 540]
	#vertices = np.append(right_bottom, [apex, left_bottom])
	vertices = np.array([right_bottom, apex, left_bottom], np.int32)

	cv2.fillPoly(mask, [vertices], ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
	masked_image = cv2.bitwise_and(img, mask)
	return masked_image



clip = VideoFileClip('./solidWhiteRight.mp4')

output_file = 'test_video.mp4'

output_stream = clip.fl_image(process_image)
output_stream.write_videofile(output_file, audio=False)







