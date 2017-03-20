##Term 1, Project 1
#**Finding Lane Lines on the Road** 

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

###1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps. First, I converted the images to grayscale, then I .... 

Finally, the two lines are drawn onto the original picture.



In order to draw a single line on the left and right lanes, I modified the draw_lines() function by ...

averaging the line segments on the left lane $\{(m_i, b_i)\mid i=1,\ldots;N_\mathrm{left}\}$ and the line segments of the right lane $\{(\mu_j,\beta_j)\mid 1,\ldots,N_\mathrm{right}\}$.  

$y = m_i x + b_i, \quad i = 1,\ldots N_\mathrm{left},$

$y = \mu_j x + \beta_j, \quad j = 1,\ldots, N_\mathrm{right}$.

$\overline{m} := (\sum_{i=1}^{N_\mathrm{left}} m_i)/N_\mathrm{left}$

$\overline{\mu} := (\sum_{j=1}^{N_\mathrm{left}} \mu_j)/N_\mathrm{left}$

If you'd like to include images to show how the pipeline works, here is how to include an image: 

$b_i = y -m_i x$

$\overline{b}$ and $\overline{\beta}$ as the averages over $b_i$, $\beta_j$.


$x = (y-b_i)/m_i$

Assuming in both cases $m_i, \mu_j\not=0$ naturally.

Setting 

The mask consists of an polygon (a trapezoid)  with the vertices (960,540), (500,325),(460,325), and (0,540). 

We may set $y_\mathrm{top}=325$ and $y_\mathrm{bottom}=540$
$x_\ast = (y_\ast-\overline{b})/\overline{m}$
with $\ast=\mathrm{top, bottom}$.
$x_\ast = (y_\ast-\overline{\beta})/\overline{\mu}$


**Stage 1: Grayscale**

![alt text][image1]

**Stage 2: Gaussian Blur**
**Stage 3: Canny Edge**
**Stage 4: Region of Interest**
**Stage 5: Hough Lines**
**Stage 6: Adding Weighted Images**


###2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when ... 

The application only for 

Another shortcoming could be ...


###3. Suggest possible improvements to your pipeline

Of course, the lane finder only allows to detect the lanes when the vehicle is travelling in the middle of a lane on a road without i.e. a highway or "autobahn".  Another shortcoming is the situation of denser traffic, i.e. if a other vehicle closes from the front.  

Of course, for real-time applications, the algorithm has to be optimized.  Two contraints: resources and time of verarbeitung.



One idea to improve the the lane representation is to average the lanes temporarily.  This could smoothen the drawing of the lanes.


A possible improvement would be to ...

Another potential improvement could be to ...