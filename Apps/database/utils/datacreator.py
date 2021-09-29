"""
Dataset creator pipeline

"""
# imports
import numpy as np
import sys
from PIL import Image, ImageDraw
from random import randint
from math import sqrt


class circle_gen():
 
    def __init__(self, width, height, count_light, count_dark, path_to_images):
        self.image_count_light = count_light
        self.image_count_dark = count_dark
        self.path_to_images = path_to_images
        self.current_file_count = 1
        self.width = width
        self.height = height


    def min_max(self):
        # number of creating objects in mind
        return randint(5, 15)


    def create_image_with_background(self, background_color):
        # background, foreground change all in grayscale
        red = 0
        blue = 0
        green = 0

        if(background_color == "light"):
            red = randint(0, 30)
            blue = randint(0, 30)
            green = randint(0, 30)
        elif (background_color == "dark"):
            red = randint(160, 240)
            blue = randint(160, 240)
            green = randint(160, 240)
            
        image = Image.new('RGBA', (self.width, self.height), (red, blue, green))
        return image


    def save_img(self, image):
        image.save(self.path_to_images + "/circles_training_dataset_" + str(self.current_file_count) + ".png")
        self.current_file_count = self.current_file_count + 1     


    def save_annotation(self, data):
        # save center (x, y), radius
        [x, y, r] = data

        with open("../dataset/test/annotations/annotations.txt", "a") as annotations:
            line = "[(" + str(x) + ", " + str(y) + "), " + str(r) + "]\n"
            annotations.write(line) 

        annotations.close()


    def circle_radius_set(self):
        return randint(5, 50)

    
    def random_center_position_and_radius(self):
        x = randint(25, 575)
        y = randint(25, 375)
        r = self.circle_radius_set()
        return [x, y, r]

    def draw_random_circles(self):
        # circle size change, numbers, contrast, then save_img, then save_annotation
        circles_created = []
        for i in range(self.image_count_light):
            print("inside light, i = " + str(i))
            new_image = self.create_image_with_background("light")
            draw = ImageDraw.Draw(new_image)
            for y in range(self.min_max()):
                print("inside for in light, y = " + str(y))
                while True:               
                    [x, y, r] = self.random_center_position_and_radius()
                    if(len(circles_created) == 0 or not (self.is_intersecting_some_circle_or_boundary(circles_created, [x, y, r]))):
                        draw.ellipse((x - r, y - r, x + r, y + r), fill=self.generate_fill("dark"), width=1)
                        circles_created.append([x, y, r])
                        self.save_annotation([x, y, r])
                        break
            self.save_img(new_image)
        for i in range(self.image_count_dark):
            print("inside dark, i = " + str(i))
            new_image = self.create_image_with_background("dark")
            draw = ImageDraw.Draw(new_image)
            for y in range(self.min_max()):
                print("inside for in dark, y = " + str(y))
                while True:               
                    [x, y, r] = self.random_center_position_and_radius()
                    if(len(circles_created) == 0 or not (self.is_intersecting_some_circle_or_boundary(circles_created, [x, y, r]))):
                        draw.ellipse((x - r, y - r, x + r, y + r), fill=self.generate_fill("light"), width=1)
                        circles_created.append([x, y, r])
                        self.save_annotation([x, y, r])
                        break
            self.save_img(new_image)


    def is_intersecting_some_circle_or_boundary(self, array_of_circles, new_circle):
        for circle in array_of_circles:
            if(self.are_two_circles_intersecting(new_circle, circle) or
            self.is_intersecting_boundary(new_circle)):
                return True           
        return False


    def are_two_circles_intersecting(self, new_circle, circle):
        [new_x, new_y, new_r] = new_circle
        [x, y, r] = circle

        dist_between_centers = sqrt(((new_x - x) ** 2) + ((new_y - y) ** 2))

        return dist_between_centers <= (new_r + r)


    def is_intersecting_boundary(self, new_circle):
        [new_x, new_y, new_r] = new_circle

        return ((new_x + new_r >= self.width) or (new_x - new_r <= 0) or 
                (new_y + new_r >= self.height) or (new_y - new_r <= 0))


    def generate_fill(self, contrast):
        red = 0
        blue = 0
        green = 0

        if(contrast == "light"):
            red = randint(0, 30)
            blue = randint(0, 30)
            green = randint(0, 30)
        elif (contrast == "dark"):
            red = randint(160, 240)
            blue = randint(160, 240)
            green = randint(160, 240)
        
        return (red, blue, green)


#main start of application for image generation

circle_files = circle_gen(600, 400, 1, 1, "../dataset/test/new_circles")
circle_files.draw_random_circles()

