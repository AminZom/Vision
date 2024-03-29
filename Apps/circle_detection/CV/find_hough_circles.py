# -*- coding: utf-8 -*-
"""
Aditya Intwala

This is a script to demonstrate the implementation of Hough transform function to
detect circle_detection from the image.

Input:
    img - Full path of the input image.
    r_min - Min radius circle to detect. Default is 10.
    r_max - Max radius circle to detect. Default is 200.
    delta_r - Delta change in radius from r_min to r_max. Default is 1.
    num_thetas - Number of steps for theta from 0 to 2PI. Default is 100.
    bin_threshold - Thresholding value in percentage to shortlist candidate for circle. Default is 0.4 i.e. 40%.
    min_edge_threshold - Minimum threshold value for edge detection. Default 100.
    max_edge_threshold - Maximum threshold value for edge detection. Default 200.

Note:
    Playing with the input parameters is required to obtain desired circle_detection in different images.
    
Returns:
    circle_img - Image with the Circles drawn
    circle_detection.txt - List of circle_detection in format (x,y,r,votes)

"""

import argparse
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from collections import defaultdict

r_min = 10
r_max = 200
delta_r = 1
num_thetas = 100
bin_threshold = 0.4

def find_hough_circles(image, r_min, r_max, delta_r, num_thetas, bin_threshold, post_process=True):
    print("in hough")
    min_edge_threshold = 100
    max_edge_threshold = 200
    # input_img = cv2.imread(image)
    # # Edge detection on the input image
    # edge_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    # ret, edge_image = cv2.threshold(edge_image, 120, 255, cv2.THRESH_BINARY_INV)
    edge_image = cv2.Canny(image, min_edge_threshold, max_edge_threshold)

    img_height, img_width = edge_image.shape[:2]
        
    # R and Theta ranges
    dtheta = int(360 / num_thetas)

    ## Thetas is bins created from 0 to 360 degree with increment of the dtheta
    thetas = np.arange(0, 360, step=dtheta)

    ## Radius ranges from r_min to r_max
    rs = np.arange(r_min, r_max, step=delta_r)

    # Calculate Cos(theta) and Sin(theta) it will be required later
    cos_thetas = np.cos(np.deg2rad(thetas))
    sin_thetas = np.sin(np.deg2rad(thetas))

    # Evaluate and keep ready the candidate circle_detection dx and dy for different delta radius
    # based on the the parametric equation of circle.
    # x = x_center + r * cos(t) and y = y_center + r * sin(t),
    # where (x_center,y_center) is Center of candidate circle with radius r. t in range of [0,2PI)
    circle_candidates = []
    for r in rs:
        for t in range(num_thetas):
            # instead of using pre-calculated cos and sin theta values you can calculate here itself by following
            # circle_candidates.append((r, int(r*cos(2*pi*t/num_thetas)), int(r*sin(2*pi*t/num_thetas))))
            # but its better to pre-calculate and use it here.
            circle_candidates.append((r, int(r * cos_thetas[t]), int(r * sin_thetas[t])))

    # Hough Accumulator, we are using defaultdic instead of standard dict as this will initialize for key which is not
    # aready present in the dictionary instead of throwing exception.
    accumulator = defaultdict(int)

    for y in range(img_height):
        for x in range(img_width):
            if edge_image[y][x] != 0:  # white pixel
                # Found an edge pixel so now find and vote for circle from the candidate circle_detection passing through this pixel.
                for r, rcos_t, rsin_t in circle_candidates:
                    x_center = x - rcos_t
                    y_center = y - rsin_t
                    accumulator[(x_center, y_center, r)] += 1  # vote for current candidate

    # Output image with detected lines drawn
    output_img = np.array(image).copy()
    # Output list of detected circle_detection. A single circle would be a tuple of (x,y,r,threshold)
    out_circles = []

    # Sort the accumulator based on the votes for the candidate circle_detection
    for candidate_circle, votes in sorted(accumulator.items(), key=lambda i: -i[1]):
        x, y, r = candidate_circle
        current_vote_percentage = votes / num_thetas
        if current_vote_percentage >= bin_threshold:
            # Shortlist the circle for final result
            out_circles.append((x, y, r, current_vote_percentage))
            print(x, y, r, current_vote_percentage)

    # Post process the results, can add more post processing later.
    if post_process:
        pixel_threshold = 5
        postprocess_circles = []
        for x, y, r, v in out_circles:
            # Exclude circle_detection that are too close of each other
            # all((x - xc) ** 2 + (y - yc) ** 2 > rc ** 2 for xc, yc, rc, v in postprocess_circles)
            # Remove nearby duplicate circle_detection based on pixel_threshold
            if all(abs(x - xc) > pixel_threshold or abs(y - yc) > pixel_threshold or abs(r - rc) > pixel_threshold for
                   xc, yc, rc, v in postprocess_circles):
                postprocess_circles.append((x, y, r, v))
        out_circles = postprocess_circles

    # Draw shortlisted circle_detection on the output image
    for x, y, r, v in out_circles:
        output_img = cv2.circle(output_img, (x, y), r, (0, 255, 0), 2)

    circle_file = open('circles_list.txt', 'w')
    circle_file.write('x ,\t y,\t Radius,\t Threshold \n')
    for i in range(len(out_circles)):
        circle_file.write(
            str(out_circles[i][0]) + ' , ' + str(out_circles[i][1]) + ' , ' + str(out_circles[i][2]) + ' , ' + str(
                out_circles[i][3]) + '\n')
    circle_file.close()

    if output_img is not None:
        cv2.imwrite("circles_img.png", output_img)
    if edge_image is None:
        print("Error in input image!")

    print("Detecting Hough Circles Complete!")
    return output_img, out_circles

# def main():
    img_path = None
    r_min = 10
    r_max = 200
    delta_r = 1
    num_thetas = 100
    bin_threshold = 0.4
    min_edge_threshold = 100
    max_edge_threshold = 200

    input_img = cv2.imread(img_path)

    # Edge detection on the input image
    edge_image = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    # ret, edge_image = cv2.threshold(edge_image, 120, 255, cv2.THRESH_BINARY_INV)
    edge_image = cv2.Canny(edge_image, min_edge_threshold, max_edge_threshold)

    cv2.imshow('Edge Image', edge_image)
    cv2.waitKey(0)

    if edge_image is not None:

        print("Detecting Hough Circles Started!")
        circle_img, circles = find_hough_circles(input_img, edge_image, r_min, r_max, delta_r, num_thetas,
                                                 bin_threshold)

        cv2.imshow('Detected Circles', circle_img)
        cv2.waitKey(0)

        circle_file = open('circles_list.txt', 'w')
        circle_file.write('x ,\t y,\t Radius,\t Threshold \n')
        for i in range(len(circles)):
            circle_file.write(
                str(circles[i][0]) + ' , ' + str(circles[i][1]) + ' , ' + str(circles[i][2]) + ' , ' + str(
                    circles[i][3]) + '\n')
        circle_file.close()

        if circle_img is not None:
            cv2.imwrite("circles_img.png", circle_img)
    else:
        print("Error in input image!")

    print("Detecting Hough Circles Complete!")


if __name__ == "__main__":
    find_hough_circles()
