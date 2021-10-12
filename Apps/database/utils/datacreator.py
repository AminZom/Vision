"""
Dataset creator pipeline

"""
################### Next to do items #######################
# circle_radius_set -> update to a dynamic and relatable number e.g. WRT image size
# half moon shaped (<50% filled) circles
# dynamic color on generate_outline method - 10% of the entire dataset
# review hard and easy cases

from PIL import Image, ImageDraw, ImageOps
from random import randint
from math import sqrt


class CircleGen:

    def __init__(self, width, height, count_light, count_dark, path_to_directory):
        self.width = width
        self.height = height
        self.image_count_light = count_light
        self.image_count_dark = count_dark
        self.path_to_directory = path_to_directory
        self.current_file_count = 1

    def num_object(self):
        # number of creating objects/circles in an image
        return randint(5, 15)

    def create_image_with_background(self, background_color):
        # background, foreground change all in grayscale
        red = 0
        blue = 0
        green = 0

        if background_color == "light":
            red = randint(0, 30)
            blue = randint(0, 30)
            green = randint(0, 30)
        elif background_color == "dark":
            red = randint(160, 240)
            blue = randint(160, 240)
            green = randint(160, 240)

        image = Image.new('RGBA', (self.width, self.height), (red, blue, green))
        image = ImageOps.grayscale(image)
        return image

    def save_img(self, image):
        image.save(self.path_to_directory + "/images/circles_dataset_" + str(self.current_file_count) + ".png")

    def save_annotation(self, data):
        # save center (x, y), radius
        [x, y, r] = data
        with open(self.path_to_directory + "/annotations/annotations_" + str(self.current_file_count) + ".txt",
                  "a") as annotations:
            line = "[(" + str(x) + ", " + str(y) + "), " + str(r) + "]\n"
            annotations.write(line)
        annotations.close()

    def circle_radius_set(self):
        # update to a dynamic and relatable number
        return randint(5, 50)

    def random_center_position_and_radius(self, margin):
        margin = int(margin)
        x = randint(margin, self.width - margin)
        y = randint(margin, self.height - margin)
        r = self.circle_radius_set()
        return [x, y, r]

    def draw_random_circles(self):
        # circle size change, numbers, contrast, then save_img, then save_annotation
        circles_created = []
        for i in range(self.image_count_light):
            print("inside light, i = " + str(i))
            new_image = self.create_image_with_background("light")
            draw = ImageDraw.Draw(new_image)
            for y in range(self.num_object()):
                print("inside for in light, y = " + str(y))
                while True:
                    [x, y, r] = self.random_center_position_and_radius(25)
                    if (len(circles_created) == 0 or not (
                            self.is_intersecting_some_circle_or_boundary(circles_created, [x, y, r]))):
                        draw.ellipse((x - r, y - r, x + r, y + r), fill=str(self.generate_fill("dark")),
                                     width=self.generate_width(r))
                        circles_created.append([x, y, r])
                        self.save_annotation([x, y, r])
                        break
            self.save_img(new_image)
            self.current_file_count = self.current_file_count + 1
        for i in range(self.image_count_dark):
            print("inside dark, i = " + str(i))
            new_image = self.create_image_with_background("dark")
            draw = ImageDraw.Draw(new_image)
            for y in range(self.num_object()):
                print("inside for in dark, y = " + str(y))
                while True:
                    [x, y, r] = self.random_center_position_and_radius(25)
                    if (len(circles_created) == 0 or not (
                            self.is_intersecting_some_circle_or_boundary(circles_created, [x, y, r]))):
                        draw.ellipse((x - r, y - r, x + r, y + r), fill=str(self.generate_fill("light")),
                                     width=self.generate_width(r))
                        circles_created.append([x, y, r])
                        self.save_annotation([x, y, r])
                        break
            self.save_img(new_image)
            self.current_file_count = self.current_file_count + 1

    def is_intersecting_some_circle_or_boundary(self, array_of_circles, new_circle):
        for circle in array_of_circles:
            if (self.are_two_circles_intersecting(new_circle, circle) or
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
        # generating RBG colors and then convert to HEX value
        red = 0
        blue = 0
        green = 0

        if contrast == "light":
            red = randint(0, 30)
            blue = randint(0, 30)
            green = randint(0, 30)
        elif contrast == "dark":
            red = randint(160, 240)
            blue = randint(160, 240)
            green = randint(160, 240)

        return "#" + '{:X}{:X}{:X}'.format(int(red / 255), int(blue / 255), int(green / 255))

    def generate_width(self, radius):
        # less than 25% of the radius
        return randint(1, int(radius / 4)) if int(radius / 4) >= 1 else 1

    def generate_outline(self):
        # fill outline of the circle with darker/lighter color WRT background and foreground
        return None

# main start of application for image generation
circle_files = CircleGen(600, 400, 1, 1, "Apps/database/dataset/test")
circle_files.draw_random_circles()
